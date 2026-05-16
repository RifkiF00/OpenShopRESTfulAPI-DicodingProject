from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from openShop.models import Category, Seller, Product, Review, Order, OrderItem
import uuid

class CategoryTestCase(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            slug='electronics',
            description='Electronic products'
        )
    
    def test_list_categories(self):
        response = self.client.get('/api/products/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_category(self):
        response = self.client.get(f'/api/products/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')

class SellerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller1', email='seller@test.com', password='pass123')
        self.seller = Seller.objects.create(
            user=self.user,
            shop_name='My Shop',
            shop_slug='my-shop'
        )
    
    def test_list_sellers(self):
        response = self.client.get('/api/products/sellers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_seller_products(self):
        response = self.client.get(f'/api/products/sellers/{self.seller.id}/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ProductTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller1', password='pass123')
        self.seller = Seller.objects.create(user=self.user, shop_name='Shop1', shop_slug='shop1')
        self.category = Category.objects.create(name='Cat1', slug='cat1')
        self.product = Product.objects.create(
            name='Product 1',
            seller=self.seller,
            category=self.category,
            price=100,
            sku='SKU001',
            description='Test product',
            location='Jakarta',
            stock=10
        )
    
    def test_list_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filter_by_price(self):
        response = self.client.get('/api/products/?min_price=50&max_price=150')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_product(self):
        response = self.client.get('/api/products/?search=Product')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_product(self):
        response = self.client.get(f'/api/products/{self.product.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Product 1')

class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.seller = Seller.objects.create(
            user=User.objects.create_user(username='seller1', password='pass123'),
            shop_name='Shop1',
            shop_slug='shop1'
        )
        self.category = Category.objects.create(name='Cat1', slug='cat1')
        self.product = Product.objects.create(
            name='Product 1',
            seller=self.seller,
            category=self.category,
            price=100,
            sku='SKU001',
            description='Test',
            location='Jakarta',
            stock=10
        )
    
    def test_add_review(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'rating': 5,
            'title': 'Great product',
            'comment': 'Love it!'
        }
        response = self.client.post(f'/api/products/{self.product.id}/add_review/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_reviews(self):
        Review.objects.create(
            product=self.product,
            reviewer=self.user,
            rating=4,
            comment='Good'
        )
        response = self.client.get(f'/api/products/{self.product.id}/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class OrderTestCase(APITestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='customer1', password='pass123')
        self.seller_user = User.objects.create_user(username='seller1', password='pass123')
        self.seller = Seller.objects.create(user=self.seller_user, shop_name='Shop1', shop_slug='shop1')
        self.category = Category.objects.create(name='Cat1', slug='cat1')
        self.product = Product.objects.create(
            name='Product 1',
            seller=self.seller,
            category=self.category,
            price=100,
            sku='SKU001',
            description='Test',
            location='Jakarta',
            stock=10,
            status='active'
        )
    
    def test_create_order(self):
        self.client.force_authenticate(user=self.customer)
        data = {
            'seller_id': str(self.seller.id),
            'items': [
                {
                    'product_id': str(self.product.id),
                    'quantity': 2
                }
            ]
        }
        response = self.client.post('/api/products/orders/create_order/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'pending')
    
    def test_order_status_update(self):
        self.client.force_authenticate(user=self.customer)
        order = Order.objects.create(
            order_number='ORD001',
            customer=self.customer,
            seller=self.seller,
            total_amount=200,
            final_amount=200,
            status='pending'
        )
        
        data = {'status': 'processing'}
        response = self.client.post(f'/api/products/orders/{order.id}/update_status/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
