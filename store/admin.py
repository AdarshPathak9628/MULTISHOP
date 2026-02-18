"""
====================================================
MULTISHOP - Admin Panel
Author  : Adarsh Pathak
====================================================
"""
from django.contrib import admin
from .models import (
    Category, Vendor, Product,
    Cart, BillingAddress,
    Order, OrderItem, Profile
)
#  OLD: from .models import vendor_images
# WHY:  Only imported one model — rest were commented out
#  NEW: Import ALL models so we can manage everything
#         from admin panel


# ============================================================
# CATEGORY ADMIN
#  OLD: Was completely commented out — could not manage
#         categories from admin panel at all!
# NEW: Fully working with search and auto-slug
# ============================================================
@admin.register(Category)
#  Using @admin.register decorator — modern professional way
#  OLD: admin.site.register(Category, CategoryAdmin)
#         Old way, less clean code
class CategoryAdmin(admin.ModelAdmin):
    # Columns shown in admin list page
    list_display = ['name', 'slug']

    #  Auto-fills slug when you type name
    # Saves time, no need to type slug manually
    prepopulated_fields = {'slug': ('name',)}

    # Search bar in admin
    search_fields = ['name']


# ============================================================
# VENDOR ADMIN
#  OLD: class VendorAdmin only showed name and image
#         Used wrong model name 'vendor_images'
#  NEW: Shows all important vendor info
#         Can approve vendors directly from list
# ============================================================
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    #  Shows more useful columns than old code
    list_display  = ['shop_name', 'user', 'phone', 'is_approved']

    #  Filter vendors by approval status
    list_filter   = ['is_approved']

    #  Can approve vendor directly from list page
    #  OLD: Had to click each vendor to approve
    list_editable = ['is_approved']

    search_fields = ['shop_name']


# ============================================================
# PRODUCT ADMIN
#  OLD: Was completely commented out!
#  NEW: Full product management with filters
# ============================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'price',
                     'stock', 'is_available', 'is_featured']

    #  Filter by category, availability
    list_filter   = ['is_available', 'is_featured', 'category']

    search_fields = ['name']

    #  Auto-fill slug from product name
    prepopulated_fields = {'slug': ('name',)}

    #  Edit price/stock directly from list — saves time!
    list_editable = ['price', 'stock', 'is_available']


# ============================================================
# ORDER ITEMS shown INSIDE Order page
#  NEW: When you open an order you can see all
#         products inside that order on same page
#  OLD: OrderItem was completely commented out!
# ============================================================
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# ============================================================
# ORDER ADMIN
#  OLD: No order management at all
#  NEW: See all orders, update status easily
# ============================================================
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'total_amount',
                     'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['user__username']

    #  Change order status directly from list
    list_editable = ['status']

    #  Show items inside each order
    inlines       = [OrderItemInline]


# ============================================================
# CART ADMIN
#  OLD: No cart management at all
#  NEW: See what users have in their carts
# ============================================================
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display  = ['user', 'product', 'quantity', 'created_at']
    search_fields = ['user__username', 'product__name']


# ============================================================
# BILLING ADDRESS ADMIN
# ============================================================
@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    list_display  = ['user', 'first_name', 'last_name',
                     'city', 'country']
    search_fields = ['first_name', 'last_name']


# ============================================================
# PROFILE ADMIN
#  OLD: No user profile management
#  NEW: See all user profiles
# ============================================================
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'phone', 'city', 'country']
    search_fields = ['user__username']