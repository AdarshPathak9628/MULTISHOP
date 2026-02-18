"""
====================================================
MULTISHOP - Professional Models
Author  : Adarsh Pathak
GitHub  : AdarshPathak9628
====================================================

OLD CODE PROBLEMS:
1. Storing passwords directly in database = HUGE security risk
   Hackers can steal all passwords if database is hacked
   Django has built-in User model with hashed passwords

2. Using snake_case for Model class names (admin_signupform)
   Django convention = PascalCase (AdminSignupForm)
   But we don't need custom signup models at all!

3. Storing admin/user as separate models = wrong approach
   Django already has User + permissions system built in
   We just extend it with a Profile model

4. Bad variable names like 'cust', 'user_id' as ForeignKey
   'cust' is abbreviation = confusing for other developers
   ForeignKey field named 'user_id' is misleading
====================================================
"""

from django.db import models
from django.contrib.auth.models import User
# Using Django's built-in User model
# OLD: Created custom User_SignupForm and admin_signupform
# WHY: Django's User already has username, email, password (hashed!),
#      is_active, is_staff, is_superuser built in
#      Never store passwords yourself in the database!


# ============================================================
# TABLE 1: CATEGORY
# ============================================================
class Category(models.Model):

    # Added slug for SEO-friendly URLs like /category/electronics/
    # OLD: No slug — URLs would be ugly like /category/1/
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    # Renamed upload folder to 'categories/' (plural, consistent)
    # OLD: 'category_images/' — inconsistent naming style
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'  #  Correct plural in admin panel
        ordering = ['name']

    def __str__(self):
        return self.name


# ============================================================
# TABLE 2: VENDOR
#  OLD: vendor_images model only stored name + image
#  NEW: Full vendor profile with all needed information
# WHY: A vendor needs shop info, approval status, contact etc.
# ============================================================
class Vendor(models.Model):

    #  OneToOne link to Django User (handles login/password)
    #  OLD: No login system for vendors at all
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='vendor'
    )

    shop_name = models.CharField(max_length=200)

    #  Renamed to 'vendors/' consistent with other upload folders
    #  OLD: 'vendor_images/' — inconsistent naming
    image = models.ImageField(upload_to='vendors/', blank=True, null=True)

    description = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)

    #  Admin can approve/reject vendors
    #  OLD: No approval system
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def __str__(self):
        # ✅ Returns shop name so admin panel is readable
        return self.shop_name


# ============================================================
# TABLE 3: PRODUCT
# ============================================================
class Product(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True, blank=True
    )

    name = models.CharField(max_length=200)

    #  Slug for clean URLs like /product/iphone-15/
    #  OLD: No slug
    slug = models.SlugField(max_length=200, unique=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    #  Optional sale price
    #  OLD: No discount system
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True, null=True
    )

    #  Renamed upload folder to 'products/' (consistent naming)
    #  OLD: 'products_images/' — inconsistent with other folders
    image = models.ImageField(upload_to='products/')

    #  PositiveIntegerField — stock cannot be negative!
    #  OLD: IntegerField — could save -5 stock which makes no sense
    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    #  Helper method to check if product is on sale
    def is_on_sale(self):
        return self.discount_price is not None

    #  Returns actual price (discounted or normal)
    def get_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price


# ============================================================
# TABLE 4: CART
#  OLD NAME: cart_storage — unclear what it stores
#  NEW NAME: Cart — clear and professional
#  OLD: used 'cust' as variable name — bad abbreviation
#  NEW: use 'user' — clear and readable
# ============================================================
class Cart(models.Model):

    #  Using Django's built-in User
    #  OLD: ForeignKey to custom User_SignupForm
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
        #  OLD: was named 'cust' — nobody knows what 'cust' means
        #  NEW: 'user' — clear for every developer
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    #  Renamed from 'product_qty' to 'quantity'
    #  OLD: 'product_qty' — abbreviation, not professional
    quantity = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return f"{self.user.username} → {self.product.name}"

    def get_total(self):
        return self.product.get_price() * self.quantity


# ============================================================
# TABLE 5: BILLING ADDRESS
# ============================================================
class BillingAddress(models.Model):

    #  Renamed from 'user_id' to 'user'
    #  OLD: ForeignKey named 'user_id' is WRONG
    # WHY: Django automatically adds _id to ForeignKey fields
    #      So 'user_id' becomes 'user_id_id' in database!
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='billing_addresses'
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default='India')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.city}"


# ============================================================
# TABLE 6: ORDER
#  OLD: Order had product directly linked (wrong!)
#  NEW: Order → OrderItem → Product (correct relationship)
# WHY: One order can have MANY products
#      Old way only allowed 1 product per order!
# ============================================================
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending',    'Pending'),
        ('processing', 'Processing'),
        ('shipped',    'Shipped'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    billing_address = models.ForeignKey(
        BillingAddress,
        on_delete=models.SET_NULL,
        null=True
    )

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} — {self.user.username}"


# ============================================================
# TABLE 7: ORDER ITEM
#  Each product in an order gets its own row
#  OLD: This was commented out! Orders had no items!
# ============================================================
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    #  Store price at time of purchase
    # WHY: Product price might change later
    #      We need to remember what customer actually paid
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

    def get_total(self):
        return self.price * self.quantity


# ============================================================
# TABLE 8: USER PROFILE
#  OLD: User_SignupForm stored passwords in plain text!
#  NEW: Profile just stores EXTRA info about the user
# WHY: Django User handles login/password safely
#      We only store additional data here
# ============================================================
class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    image = models.ImageField(
        upload_to='profiles/',
        #  Renamed from 'user_profile_image/' to 'profiles/'
        #  OLD: 'user_profile_image/' — too long, inconsistent
        blank=True, null=True
    )

    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True, default='India')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"