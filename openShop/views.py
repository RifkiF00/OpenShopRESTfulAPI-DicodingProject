from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.exceptions import PermissionDenied, ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Q, Count
from django.utils.text import slugify
from django.http import Http404
from openShop.models import (
    Product, Category, Seller, Review, Order, OrderItem, StockHistory
)
from openShop.serializers import (
    ProductDetailSerializer, ProductListSerializer, CategorySerializer,
    SellerSerializer, ReviewSerializer, OrderSerializer, OrderItemSerializer,
    StockHistorySerializer
)
import uuid
from datetime import datetime

class StandardResultsSetPagination:
    def paginate_queryset(self, queryset, request, view=None):
        return list(queryset)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user and self.request.user.is_staff:
            return Category.objects.all()
        return Category.objects.filter(is_active=True)

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.filter(is_active=True)
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_verified', 'rating']
    search_fields = ['shop_name', 'description']
    ordering_fields = ['rating', 'total_sold', 'created_at']
    ordering = ['-rating']
    
    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        seller = self.get_object()
        products = seller.products.filter(is_delete=False, status='active')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'seller', 'status', 'is_available']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'rating', 'total_sold', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_delete=False, status='active')
        
        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Discount filter
        min_discount = self.request.query_params.get('min_discount')
        if min_discount:
            queryset = queryset.filter(discount__gte=min_discount)
        
        # Rating filter
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=min_rating)
        
        # Location filter
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset.distinct()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'seller_profile'):
            raise PermissionDenied("Anda harus menjadi seller untuk membuat produk")
        serializer.save(seller=self.request.user.seller_profile)
    
    def perform_update(self, serializer):
        product = self.get_object()
        if product.seller.user != self.request.user:
            raise PermissionDenied("Anda hanya bisa update produk milik Anda")
        serializer.save()
    
    def perform_destroy(self, instance):
        if instance.seller.user != self.request.user:
            raise PermissionDenied("Anda hanya bisa hapus produk milik Anda")
        instance.is_delete = True
        instance.save()
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        product = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, reviewer=request.user)
            
            # Update product rating
            avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg']
            product.rating = round(avg_rating, 2) if avg_rating else 0
            product.total_reviews = product.reviews.count()
            product.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        
        # Filter by rating
        min_rating = request.query_params.get('min_rating')
        if min_rating:
            reviews = reviews.filter(rating__gte=min_rating)
        
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stock_history(self, request, pk=None):
        product = self.get_object()
        history = product.stock_history.all()
        
        page = self.paginate_queryset(history)
        if page is not None:
            serializer = StockHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = StockHistorySerializer(history, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        if not self.request.user.is_staff:
            raise PermissionDenied("Hanya admin yang bisa adjust stok")
        
        product = self.get_object()
        quantity = request.data.get('quantity')
        notes = request.data.get('notes', '')
        
        if quantity is None:
            raise ValidationError({'quantity': 'Quantity diperlukan'})
        
        old_stock = product.stock
        product.stock += quantity
        product.save()
        
        StockHistory.objects.create(
            product=product,
            transaction_type='adjustment',
            quantity=quantity,
            previous_stock=old_stock,
            new_stock=product.stock,
            notes=notes,
            created_by=request.user
        )
        
        return Response({'status': 'success', 'message': 'Stok diupdate'})

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'rating']
    ordering_fields = ['rating', 'helpful_count', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        raise ValidationError("Gunakan endpoint /products/{id}/add_review/ untuk membuat review")
    
    @action(detail=True, methods=['post'])
    def mark_helpful(self, request, pk=None):
        review = self.get_object()
        review.helpful_count += 1
        review.save()
        return Response({'helpful_count': review.helpful_count})

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    ordering_fields = ['created_at', 'total_amount']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer=self.request.user)
    
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        customer = request.user
        seller_id = request.data.get('seller_id')
        items_data = request.data.get('items', [])
        
        if not seller_id or not items_data:
            raise ValidationError({'error': 'seller_id dan items diperlukan'})
        
        try:
            seller = Seller.objects.get(id=seller_id)
        except Seller.DoesNotExist:
            raise ValidationError({'seller_id': 'Seller tidak ditemukan'})
        
        total_amount = 0
        discount_amount = 0
        order_items = []
        
        for item in items_data:
            try:
                product = Product.objects.get(id=item['product_id'])
                quantity = item['quantity']
                
                if product.stock < quantity:
                    raise ValidationError(f'{product.name} stok tidak cukup')
                
                price = float(product.price)
                discount = product.discount
                subtotal = price * quantity * (1 - discount / 100)
                
                total_amount += price * quantity
                discount_amount += (price * quantity * discount / 100)
                
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price_at_purchase': price,
                    'discount_at_purchase': discount,
                    'subtotal': subtotal
                })
            except Product.DoesNotExist:
                raise ValidationError(f'Product {item.get("product_id")} tidak ditemukan')
        
        final_amount = total_amount - discount_amount
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            order_number=order_number,
            customer=customer,
            seller=seller,
            total_amount=total_amount,
            discount_amount=discount_amount,
            final_amount=final_amount,
            status='pending',
            payment_status='unpaid'
        )
        
        for item in order_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_purchase=item['price_at_purchase'],
                discount_at_purchase=item['discount_at_purchase'],
                subtotal=item['subtotal']
            )
            
            product = item['product']
            product.stock -= item['quantity']
            product.total_sold += item['quantity']
            product.save()
            
            StockHistory.objects.create(
                product=product,
                transaction_type='out',
                quantity=item['quantity'],
                previous_stock=product.stock + item['quantity'],
                new_stock=product.stock,
                notes=f'Order {order_number}',
                created_by=customer
            )
        
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            raise ValidationError({'status': 'Status diperlukan'})
        
        if new_status == 'shipped':
            order.shipped_at = datetime.now()
        elif new_status == 'delivered':
            order.delivered_at = datetime.now()
        
        order.status = new_status
        order.save()
        
        serializer = self.get_serializer(order)
        return Response(serializer.data)

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.request.query_params.get('order_id')
        if order_id:
            return OrderItem.objects.filter(order_id=order_id)
        return OrderItem.objects.none()

class StockHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StockHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product', 'transaction_type']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return StockHistory.objects.all()
        return StockHistory.objects.filter(product__seller__user=self.request.user)