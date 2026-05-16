from rest_framework import serializers
from openShop.models import (
    Product, Category, Seller, Review, Order, OrderItem, StockHistory
)
from rest_framework.reverse import reverse
from django.db.models import Avg, Count

class CategorySerializer(serializers.ModelSerializer):
    total_products = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 'total_products', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def get_total_products(self, obj):
        return obj.products.filter(is_delete=False, status='active').count()

class SellerSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    total_products = serializers.SerializerMethodField()
    
    class Meta:
        model = Seller
        fields = ['id', 'user_info', 'shop_name', 'shop_slug', 'description', 'logo', 
                  'rating', 'total_products', 'is_verified', 'is_active', 'created_at']
        read_only_fields = ['id', 'total_products', 'rating', 'created_at']
    
    def get_user_info(self, obj):
        return {
            'username': obj.user.username,
            'email': obj.user.email
        }
    
    def get_total_products(self, obj):
        return obj.products.filter(is_delete=False, status='active').count()

class ReviewSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.CharField(source='reviewer.username', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'product', 'reviewer_username', 'rating', 'title', 'comment', 
                  'is_verified_purchase', 'helpful_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'helpful_count', 'created_at', 'updated_at']

class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_info = SellerSerializer(source='seller', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    _links = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'category_name', 'seller_info', 'price', 'sku',
            'description', 'long_description', 'location', 'discount', 'stock',
            'is_available', 'picture', 'status', 'rating', 'average_rating',
            'total_reviews', 'total_sold', 'discounted_price', 'created_at', 'updated_at', '_links'
        ]
        read_only_fields = ['id', 'rating', 'total_reviews', 'total_sold', 'created_at', 'updated_at']
    
    def get_average_rating(self, obj):
        avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 2) if avg else 0
    
    def get_discounted_price(self, obj):
        return float(obj.get_discounted_price())
    
    def get__links(self, obj):
        request = self.context.get('request')
        return [
            {
                "rel": "self",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "GET",
                "types": ["application/json"]
            },
            {
                "rel": "update",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "PUT",
                "types": ["application/json"]
            },
            {
                "rel": "delete",
                "href": reverse('product-detail', kwargs={'pk': obj.pk}, request=request),
                "action": "DELETE",
                "types": ["application/json"]
            },
            {
                "rel": "reviews",
                "href": f"{reverse('product-detail', kwargs={'pk': obj.pk}, request=request)}reviews/",
                "action": "GET",
                "types": ["application/json"]
            }
        ]

class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.shop_name', read_only=True)
    discounted_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category_name', 'seller_name', 'price', 'discount',
                  'discounted_price', 'stock', 'picture', 'rating', 'total_reviews',
                  'total_sold', 'created_at']
        read_only_fields = ['id', 'rating', 'created_at']
    
    def get_discounted_price(self, obj):
        return float(obj.get_discounted_price())

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_purchase',
                  'discount_at_purchase', 'subtotal', 'created_at']
        read_only_fields = ['id', 'price_at_purchase', 'discount_at_purchase', 'subtotal', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    seller_info = SellerSerializer(source='seller', read_only=True)
    customer_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'customer_info', 'seller_info', 'status',
                  'payment_status', 'total_amount', 'discount_amount', 'shipping_cost',
                  'final_amount', 'items', 'notes', 'shipping_address', 'created_at',
                  'updated_at', 'shipped_at', 'delivered_at']
        read_only_fields = ['id', 'order_number', 'total_amount', 'final_amount',
                           'created_at', 'updated_at', 'shipped_at', 'delivered_at']
    
    def get_customer_info(self, obj):
        return {
            'username': obj.customer.username,
            'email': obj.customer.email
        }

class StockHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = StockHistory
        fields = ['id', 'product', 'product_name', 'transaction_type', 'quantity',
                  'previous_stock', 'new_stock', 'notes', 'created_by_username', 'created_at']
        read_only_fields = ['id', 'created_at']