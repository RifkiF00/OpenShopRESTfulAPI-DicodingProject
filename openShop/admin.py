from django.contrib import admin
from .models import Product, Category, Seller, Review, Order, OrderItem, StockHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'user', 'rating', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_verified', 'is_active', 'rating', 'created_at')
    search_fields = ('shop_name', 'user__username', 'user__email')
    readonly_fields = ('id', 'total_products', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'stock', 'status', 'rating', 'is_delete', 'created_at')
    list_filter = ('category', 'seller', 'status', 'is_delete', 'created_at', 'rating')
    search_fields = ('name', 'sku', 'description')
    readonly_fields = ('id', 'rating', 'total_reviews', 'total_sold', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('id', 'name', 'sku', 'seller', 'category', 'status')
        }),
        ('Pricing', {
            'fields': ('price', 'discount')
        }),
        ('Inventory', {
            'fields': ('stock', 'is_available', 'total_sold')
        }),
        ('Details', {
            'fields': ('description', 'long_description', 'picture', 'location')
        }),
        ('Ratings', {
            'fields': ('rating', 'total_reviews')
        }),
        ('Management', {
            'fields': ('is_delete', 'created_at', 'updated_at')
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'reviewer', 'rating', 'is_verified_purchase', 'helpful_count', 'created_at')
    list_filter = ('rating', 'is_verified_purchase', 'created_at')
    search_fields = ('product__name', 'reviewer__username', 'comment')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'seller', 'status', 'payment_status', 'final_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'customer__username', 'seller__shop_name')
    readonly_fields = ('id', 'order_number', 'total_amount', 'final_amount', 'created_at', 'updated_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product__name')
    readonly_fields = ('id', 'created_at')

@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'transaction_type', 'quantity', 'previous_stock', 'new_stock', 'created_by', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('product__name', 'notes')
    readonly_fields = ('id', 'created_at')
