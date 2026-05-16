# API Documentation
**Author:** Rifki Firmansyah  
**Hackathon X Digdaya Submission**

---

# OpenShop RESTful API - Complete Reference

## 🔐 Authentication

OpenShop adalah platform e-commerce modern yang dibangun dengan Django REST Framework. API ini menyediakan fitur lengkap untuk manajemen produk, kategori, penjual, pesanan, dan ulasan pelanggan.

## 📋 Table of Contents

1. [Authentication](#authentication)
2. [Base URL](#base-url)
3. [Response Format](#response-format)
4. [Endpoints](#endpoints)
5. [Error Handling](#error-handling)
6. [Advanced Features](#advanced-features)

## 🔐 Authentication

OpenShop menggunakan JWT (JSON Web Tokens) untuk autentikasi.

### Obtaining Tokens

**POST** `/api/auth/token/`

Request:
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using the Token

Add the access token to request headers:
```
Authorization: Bearer <access_token>
```

### Refreshing Token

**POST** `/api/auth/token/refresh/`

Request:
```json
{
  "refresh": "your_refresh_token"
}
```

## 🌐 Base URL

```
http://localhost:8000/api/
```

## 📦 Response Format

Semua response mengikuti format standar:

**Success Response:**
```json
{
  "id": "uuid-string",
  "name": "Product Name",
  "price": 100000,
  ...
}
```

**Error Response:**
```json
{
  "detail": "Not found.",
  "status": 404
}
```

## 🔌 Endpoints

### Authentication Endpoints

#### Register User
**POST** `/api/auth/register/register/`

Request:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepass123",
  "password2": "securepass123"
}
```

#### Get Current User Profile
**GET** `/api/auth/profile/me/`

#### Update User Profile
**PUT** `/api/auth/profile/update_profile/`

Request:
```json
{
  "phone": "0812345678",
  "address": "Jl. Example No.1",
  "city": "Jakarta",
  "province": "DKI Jakarta",
  "postal_code": "12345"
}
```

---

### Category Endpoints

#### List All Categories
**GET** `/api/products/categories/`

Query Parameters:
- `search` - Search by name or description
- `ordering` - Sort by: name, -name, created_at, -created_at

#### Get Category Details
**GET** `/api/products/categories/{id}/`

#### Create Category (Admin Only)
**POST** `/api/products/categories/`

Request:
```json
{
  "name": "Electronics",
  "slug": "electronics",
  "description": "Electronic products",
  "icon": "https://example.com/icon.png"
}
```

---

### Seller Endpoints

#### List All Sellers
**GET** `/api/products/sellers/`

Query Parameters:
- `is_verified` - true/false
- `rating` - Filter by rating
- `search` - Search by shop name
- `ordering` - Sort by: rating, -rating, total_sold, -total_sold, created_at, -created_at

#### Get Seller Details
**GET** `/api/products/sellers/{id}/`

#### Get Seller's Products
**GET** `/api/products/sellers/{id}/products/`

---

### Product Endpoints

#### List Products
**GET** `/api/products/`

Query Parameters:
- `category` - Filter by category ID
- `seller` - Filter by seller ID
- `status` - Filter by status (draft, active, inactive, discontinued)
- `min_price` - Minimum price
- `max_price` - Maximum price
- `min_discount` - Minimum discount percentage
- `min_rating` - Minimum rating
- `location` - Filter by location
- `search` - Search by name, description, SKU
- `ordering` - Sort by: price, -price, rating, -rating, total_sold, -total_sold, created_at, -created_at

#### Get Product Details
**GET** `/api/products/{id}/`

Response includes:
- Product details
- Category information
- Seller information
- Average rating
- List of reviews
- Discounted price calculation

#### Create Product (Seller Only)
**POST** `/api/products/`

Request:
```json
{
  "name": "Laptop Pro",
  "category": "category-id",
  "price": 15000000,
  "sku": "LAP001",
  "description": "High performance laptop",
  "long_description": "Detailed description...",
  "location": "Jakarta",
  "discount": 10,
  "stock": 50,
  "is_available": true,
  "picture": "https://example.com/image.jpg"
}
```

#### Update Product (Seller Only)
**PUT** `/api/products/{id}/`

#### Delete Product (Soft Delete)
**DELETE** `/api/products/{id}/`

#### Adjust Stock (Admin Only)
**POST** `/api/products/{id}/adjust_stock/`

Request:
```json
{
  "quantity": 10,
  "notes": "Restock from supplier"
}
```

#### Get Product Stock History
**GET** `/api/products/{id}/stock_history/`

---

### Review Endpoints

#### Add Review to Product
**POST** `/api/products/{id}/add_review/`

Request:
```json
{
  "rating": 5,
  "title": "Excellent product",
  "comment": "Very satisfied with this purchase"
}
```

#### Get Product Reviews
**GET** `/api/products/{id}/reviews/`

Query Parameters:
- `min_rating` - Filter by minimum rating
- `ordering` - Sort by rating or helpful count

#### Mark Review as Helpful
**POST** `/api/products/reviews/{id}/mark_helpful/`

---

### Order Endpoints

#### List Orders
**GET** `/api/products/orders/`

Query Parameters:
- `status` - Filter by order status
- `payment_status` - Filter by payment status
- `ordering` - Sort by created_at or total_amount

#### Create Order
**POST** `/api/products/orders/create_order/`

Request:
```json
{
  "seller_id": "seller-uuid",
  "items": [
    {
      "product_id": "product-uuid",
      "quantity": 2
    },
    {
      "product_id": "product-uuid-2",
      "quantity": 1
    }
  ]
}
```

Response:
```json
{
  "id": "order-uuid",
  "order_number": "ORD-ABC123DE",
  "customer_info": { "username": "customer1", "email": "customer@example.com" },
  "status": "pending",
  "payment_status": "unpaid",
  "total_amount": "300000.00",
  "discount_amount": "0.00",
  "final_amount": "300000.00",
  "items": [...],
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Order Details
**GET** `/api/products/orders/{id}/`

#### Update Order Status
**POST** `/api/products/orders/{id}/update_status/`

Request:
```json
{
  "status": "shipped"
}
```

Valid statuses: pending, processing, shipped, delivered, cancelled, returned

---

### Stock History Endpoints

#### Get Stock History
**GET** `/api/products/stock-history/`

Query Parameters:
- `product` - Filter by product ID
- `transaction_type` - Filter by type (in, out, adjustment)

---

## 🚨 Error Handling

### Common Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Data conflict (e.g., duplicate SKU) |
| 500 | Internal Server Error | Server error |

### Error Response Example

```json
{
  "detail": "Authentication credentials were not provided.",
  "status": 401
}
```

---

## 🎯 Advanced Features

### 1. Price Range Filtering

Filter products by price range:

```
GET /api/products/?min_price=100000&max_price=5000000
```

### 2. Advanced Search

Search across multiple fields:

```
GET /api/products/?search=laptop
```

### 3. Rating-Based Filtering

Get highly-rated products:

```
GET /api/products/?min_rating=4.5
```

### 4. Multiple Sorting

Sort by multiple criteria:

```
GET /api/products/?ordering=-rating,-created_at
```

### 5. Inventory Tracking

Automatic stock history tracking with every transaction:

```
GET /api/products/{id}/stock_history/
```

### 6. Order Management

Full order lifecycle management:
- Create orders with multiple items
- Track order status
- Automatic stock deduction
- Payment status tracking

### 7. Review System

- Customer reviews with ratings (1-5 stars)
- Automatic average rating calculation
- Helpful count tracking
- Verified purchase badge

---

## 📊 Pagination

List endpoints support pagination:

```
GET /api/products/?page=1&page_size=10
```

Response:
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 💻 Code Examples

### JavaScript / Fetch

```javascript
// Get access token
const getToken = async () => {
  const response = await fetch('http://localhost:8000/api/auth/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: 'user',
      password: 'pass'
    })
  });
  const data = await response.json();
  return data.access;
};

// Use token to fetch products
const getProducts = async (token) => {
  const response = await fetch('http://localhost:8000/api/products/', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

### Python / Requests

```python
import requests

# Get token
response = requests.post('http://localhost:8000/api/auth/token/', json={
    'username': 'user',
    'password': 'pass'
})
token = response.json()['access']

# Use token
headers = {'Authorization': f'Bearer {token}'}
response = requests.get('http://localhost:8000/api/products/', headers=headers)
products = response.json()
```

---

## 🔗 API Documentation URL

Swagger UI: http://localhost:8000/api/docs/
ReDoc: http://localhost:8000/api/redoc/

---

## 📝 License

MIT License
