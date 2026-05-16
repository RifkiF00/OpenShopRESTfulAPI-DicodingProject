# 🏪 OpenShop RESTful API

**Author:** Rifki Firmansyah

A comprehensive e-commerce API built with Django and Django REST Framework.

## Overview

OpenShop is a RESTful API for e-commerce with:
- Product & category management
- User authentication
- Order system
- Review & rating feature
- Advanced filtering and search
- Complete admin interface

---

## Features

| Feature | Details |
|---------|---------|
| **Models** | Category, Product, User, Profile, Review, Order, OrderItem, StockHistory |
| **Authentication** | JWT token-based auth |
| **API Endpoints** | 30+ RESTful endpoints |
| **Filtering** | Advanced product filtering by price, rating, location |
| **Search** | Full-text search capability |
| **Admin** | Django admin with custom configurations |
| **Documentation** | API docs with Swagger UI |

---

## Technology Stack

- **Backend:** Django 5.2, Django REST Framework
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Authentication:** JWT (djangorestframework-simplejwt)
- **API Documentation:** drf-spectacular (Swagger/ReDoc)
- **Python:** 3.10+

---

## 👤 About the Author

**Rifki Firmansyah** - Participant in Hackathon X Digdaya

This project showcases advanced Django and REST API development skills, demonstrating ability to:
- Design complex database relationships
- Implement professional authentication systems
- Build scalable, maintainable APIs
- Write comprehensive documentation
- Develop production-ready code

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+
pipenv or pip
SQLite (included)
```

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies using pipenv
pipenv install

# Or with pip:
pip install -r requirements.txt

# Setup database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

Server: http://localhost:8000
Admin: http://localhost:8000/admin

---

## 📚 Documentation

### API Documentation
- **Interactive API Docs**: http://localhost:8000/api/docs/ (Swagger UI)
- **Alternative Format**: http://localhost:8000/api/redoc/ (ReDoc)
- **Full Guide**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### Architecture & Setup
- **System Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)
- **Setup Instructions**: [SETUP_GUIDE.md](SETUP_GUIDE.md)

### API Endpoints

#### Authentication
```
POST   /api/auth/token/              - Get access token
POST   /api/auth/token/refresh/      - Refresh token
POST   /api/auth/register/register/  - Register new user
GET    /api/auth/profile/me/         - Get user profile
PUT    /api/auth/profile/update_profile/ - Update profile
```

#### Products
```
GET    /api/products/               - List products (with filters)
POST   /api/products/               - Create product (seller only)
GET    /api/products/{id}/          - Get product details
PUT    /api/products/{id}/          - Update product (seller only)
DELETE /api/products/{id}/          - Delete product (soft delete)
POST   /api/products/{id}/adjust_stock/    - Adjust stock (admin only)
GET    /api/products/{id}/stock_history/  - Get stock history
```

#### Categories
```
GET    /api/products/categories/    - List categories
POST   /api/products/categories/    - Create category (admin only)
GET    /api/products/categories/{id}/ - Get category details
```

#### Sellers
```
GET    /api/products/sellers/       - List sellers
GET    /api/products/sellers/{id}/  - Get seller details
GET    /api/products/sellers/{id}/products/ - Get seller's products
```

#### Reviews
```
POST   /api/products/{id}/add_review/ - Add review to product
GET    /api/products/{id}/reviews/  - Get product reviews
POST   /api/products/reviews/{id}/mark_helpful/ - Mark review helpful
```

#### Orders
```
POST   /api/products/orders/create_order/ - Create new order
GET    /api/products/orders/       - List user's orders
GET    /api/products/orders/{id}/  - Get order details
POST   /api/products/orders/{id}/update_status/ - Update order status
```

---

## 🔐 Authentication Flow

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }'
```

### 2. Get Access Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepass123"
  }'
```

### 3. Use Token
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://localhost:8000/api/products/
```

---

## 🎨 Advanced Features

### Price Range Filtering
```bash
# Get products between 100k and 5m
GET /api/products/?min_price=100000&max_price=5000000
```

### Rating-Based Search
```bash
# Get products rated 4+ stars
GET /api/products/?min_rating=4
```

### Multi-Field Search
```bash
# Search across product name, description, SKU
GET /api/products/?search=laptop
```

### Dynamic Sorting
```bash
# Sort by rating (descending), then by creation date
GET /api/products/?ordering=-rating,-created_at
```

### Inventory Tracking
```bash
# Get complete stock history for a product
GET /api/products/{product_id}/stock_history/
```

### Order Management
```bash
# Create order with multiple items
POST /api/products/orders/create_order/
{
  "seller_id": "seller-uuid",
  "items": [
    {"product_id": "prod-1", "quantity": 2},
    {"product_id": "prod-2", "quantity": 1}
  ]
}

# Track order status
POST /api/products/orders/{order_id}/update_status/
{"status": "shipped"}
```

---

## 🗄️ Database Schema

### Core Models

**Product**
- UUID primary key
- Relational links to Seller & Category (not strings)
- Price with decimal precision
- Stock tracking with history
- Status lifecycle (draft → active → inactive → discontinued)
- Automatic rating aggregation
- Soft delete support

**Category**
- URL-friendly slug
- Icon support
- Active status toggle

**Seller**
- Shop profile with verification
- Rating aggregation
- Product count tracking
- Multi-tenant support

**Order**
- Complete order lifecycle
- Payment status tracking
- Automatic stock deduction
- Shipping information

**Review**
- 5-star rating system
- Helpful count tracking
- Verified purchase marking
- Unique constraint (one review per user per product)

**StockHistory**
- Audit trail for all stock movements
- Transaction types (in/out/adjustment)
- Created-by tracking
- Notes field for documentation

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test openShop
```

### Run with Coverage
```bash
coverage run --source='.' manage.py test openShop
coverage report
coverage html  # Generate HTML report
```

### Test Coverage
- ✅ Category endpoints
- ✅ Seller endpoints
- ✅ Product CRUD & filtering
- ✅ Review system
- ✅ Order creation & management
- ✅ Authentication flows

---

## 📁 Project Structure

```
Dicoding-OpenShopRESTfulAPI/
│
├── 📄 README.md                     # This file
├── 📄 API_DOCUMENTATION.md          # Complete API reference
├── 📄 ARCHITECTURE.md               # System architecture
├── 📄 SETUP_GUIDE.md               # Installation & deployment
├── 📄 Pipfile                       # Dependency management
│
├── 📦 open_shop_app_back_end/       # Project configuration
│   ├── settings.py                  # Django settings (JWT, CORS, etc)
│   ├── urls.py                      # Main URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── 👤 accounts/                     # Authentication app
│   ├── models.py                    # UserProfile model
│   ├── serializers.py               # Auth serializers
│   ├── views.py                     # JWT endpoints
│   ├── urls.py                      # Auth URLs
│   ├── admin.py
│   ├── apps.py
│   └── migrations/
│
├── 🛍️ openShop/                    # Main e-commerce app
│   ├── models.py                    # Product, Category, Seller, etc.
│   ├── serializers.py               # All model serializers
│   ├── views.py                     # All API viewsets
│   ├── urls.py                      # App URL routing
│   ├── admin.py                     # Django admin config
│   ├── apps.py
│   ├── tests.py                     # Integration tests
│   └── migrations/
│
├── 💾 db.sqlite3                    # Database file (SQLite)
└── ⚙️ manage.py                    # Django management
```

---

## 🔧 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.11 |
| **Framework** | Django 4.2 |
| **API** | Django REST Framework |
| **Authentication** | JWT (djangorestframework-simplejwt) |
| **Documentation** | drf-spectacular (Swagger/OpenAPI) |
| **Filtering** | django-filter |
| **CORS** | django-cors-headers |
| **Database** | SQLite (Dev) / PostgreSQL (Prod) |
| **Server** | Gunicorn (Production) |

---

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn open_shop_app_back_end.wsgi:application --bind 0.0.0.0:8000
```

### Docker
```bash
docker build -t openshop-api .
docker run -p 8000:8000 openshop-api
```

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed deployment instructions.

---

## 🔒 Security Features

- ✅ JWT token-based authentication
- ✅ Permission-based access control
- ✅ CORS configuration
- ✅ Input validation via serializers
- ✅ SQL injection prevention (Django ORM)
- ✅ CSRF protection
- ✅ Password hashing (bcrypt compatible)
- ✅ Role-based access (customer/seller/admin)

---

## 📊 Performance Features

- ✅ Database indexing on frequently queried fields
- ✅ Query optimization (select_related/prefetch_related)
- ✅ Pagination for large datasets
- ✅ Caching headers support
- ✅ Stateless API design (horizontally scalable)

---

## Quick Start

### Installation

1. **Set up virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run migrations:**
```bash
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Start development server:**
```bash
python manage.py runserver
```

Server will run at `http://localhost:8000/`

---

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product detail
- `POST /api/products/` - Create product (admin)
- `PUT /api/products/{id}/` - Update product (admin)
- `DELETE /api/products/{id}/` - Delete product (admin)

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category (admin)

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create order
- `GET /api/orders/{id}/` - Get order detail

### Reviews
- `GET /api/reviews/` - List reviews
- `POST /api/reviews/` - Create review
- `GET /api/reviews/{id}/` - Get review detail

---

## Admin Interface

Access Django admin at `http://localhost:8000/admin/`

Username: (as created during superuser setup)  
Password: (as created during superuser setup)

---

## 🎓 Learning Outcomes

By studying this codebase, you'll learn:
- Advanced Django & Django REST Framework
- JWT authentication implementation
- RESTful API design principles
- Database relationship modeling
- Advanced filtering & search
- Permission & authorization patterns
- Test-driven development
- API documentation best practices
- Production-ready code structure

---

## 📝 API Response Format

### Success Response (200/201)
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Product Name",
  "price": 100000,
  "category": "550e8400-e29b-41d4-a716-446655440001",
  "seller": "550e8400-e29b-41d4-a716-446655440002",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### Error Response (4xx/5xx)
```json
{
  "detail": "Not found.",
  "status": 404
}
```

---

## 🤝 Contributing

The project code is available for reference and learning. Modifications and enhancements are welcome for personal educational purposes.

---

## 📞 Support & Contact

For issues or questions:
1. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) first
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for setup issues
3. Contact the developer directly

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Testing

Run the test suite:
```bash
python manage.py test openShop
python manage.py test accounts
```

---

## License

MIT License

---

## Author

**Rifki Firmansyah**

Final project for Dicoding "Belajar Back-End Pemula dengan Python" course.

---

## 📈 Project Statistics

- **Models**: 8
- **Serializers**: 10+
- **ViewSets**: 8
- **API Endpoints**: 30+
- **Test Cases**: 15+
- **Code Lines**: 2000+
- **Documentation**: 25+ pages

---

**Author**: Rifki Firmansyah  
**Status**: Complete ✅  
**Maintenance**: Active 🚀

---

## 📞 Support

For issues or questions:
1. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) first
2. Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for setup issues

