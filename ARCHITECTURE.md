# System Architecture
**Author:** Rifki Firmansyah  
**Hackathon X Digdaya Submission**

---

# OpenShop API - System Architecture & Design

## 📐 System Overview

### Technology Stack

- **Backend Framework**: Django 4.2
- **API Framework**: Django REST Framework
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI 3.0

### Project Structure

```
Dicoding-OpenShopRESTfulAPI/
│
├── open_shop_app_back_end/     # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py
│
├── accounts/                    # Authentication app
│   ├── models.py               # UserProfile model
│   ├── serializers.py          # User serializers
│   ├── views.py                # Auth viewsets
│   └── urls.py
│
├── openShop/                    # Main app
│   ├── models.py               # Product, Category, Seller, Order, Review
│   ├── serializers.py          # All serializers
│   ├── views.py                # All viewsets
│   ├── admin.py                # Django admin configuration
│   └── urls.py                 # App URL routing
│
└── manage.py                    # Django management script
```

## Database Schema

### Key Models

#### UserProfile
- Extends Django User model
- Stores user profile information (phone, address, role)
- Supports customer/seller/admin roles

#### Category
- Product categories (Electronics, Clothing, etc.)
- Slug for URL-friendly representation
- Tracks active status

#### Seller
- One-to-one relationship with User
- Manages shop information
- Tracks seller rating and verification status

#### Product
- Main product model
- Foreign keys to Seller and Category
- Includes pricing, inventory, and status tracking
- Automatically calculates discounted prices

#### Review
- Customer reviews for products
- Rating system (1-5 stars)
- Tracks verified purchases

#### Order
- Customer orders from sellers
- Tracks order and payment status
- Maintains order history

#### OrderItem
- Individual items in an order
- Captures price/discount at time of purchase

#### StockHistory
- Audit trail for inventory changes
- Tracks all stock movements

## API Design Patterns

### 1. RESTful Conventions

- **GET** - Retrieve data
- **POST** - Create new resources
- **PUT** - Update existing resources
- **DELETE** - Delete resources (soft delete for products)

### 2. Authentication & Authorization

- JWT tokens for API authentication
- Permission classes for endpoint protection
- Role-based access control

### 3. Response Format

All responses follow a consistent JSON format with proper HTTP status codes.

### 4. Filtering & Search

- DjangoFilterBackend for advanced filtering
- SearchFilter for text search
- Custom filtering for price ranges, ratings

### 5. Pagination

- Page-based pagination for list endpoints
- Configurable page size

### 6. Error Handling

- Standardized error responses
- Meaningful error messages
- Proper HTTP status codes

## Key Features

### Advanced Filtering

Products can be filtered by:
- Category
- Seller
- Price range (min_price, max_price)
- Discount level
- Rating
- Location
- Status
- Availability

### Inventory Management

- Real-time stock tracking
- Stock history with audit trail
- Low stock alerts capability
- Automatic stock deduction on orders

### Order Management

- Multi-item orders
- Order status workflow (pending → processing → shipped → delivered)
- Payment status tracking
- Automatic stock adjustments

### Review System

- 5-star rating system
- Average rating calculation
- Helpful count tracking
- Verified purchase marking

### Seller Features

- Shop profile management
- Product management
- Order history
- Rating/reputation system
- Verification status

## Security Considerations

- JWT token-based authentication
- Permission-based access control
- CORS configuration for frontend
- Input validation via serializers
- SQL injection prevention (Django ORM)
- CSRF protection

## Performance Optimizations

- Database indexes on frequently queried fields
- Query optimization with select_related/prefetch_related
- Pagination to limit response size
- Caching headers support

## Scalability

- Designed for multi-seller architecture
- Stateless API (easily horizontally scalable)
- Database indexing for query optimization
- Ready for microservices transition

---

## Deployment Considerations

### Environment Variables

- SECRET_KEY - Django secret key
- DEBUG - Debug mode (False in production)
- ALLOWED_HOSTS - Allowed hostnames
- DATABASE_URL - Database connection string

### Production Settings

- Use PostgreSQL instead of SQLite
- Set DEBUG = False
- Configure ALLOWED_HOSTS properly
- Use environment variables for sensitive data
- Enable HTTPS
- Configure CORS appropriately

---

## Future Enhancements

1. Payment Gateway Integration (Stripe, PayPal)
2. Email Notifications
3. Wishlist Feature
4. Product Comparison
5. Advanced Analytics
6. Real-time Notifications (WebSockets)
7. Mobile App Support
8. Multi-language Support
9. Rating & Review Moderation
10. Seller Dashboard Analytics
