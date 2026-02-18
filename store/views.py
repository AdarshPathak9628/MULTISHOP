from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Cart, Profile


def index(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(
        is_featured=True,
        is_available=True
    )[:8]
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'store/index.html', context)

def shop(request):
    return render(request, 'store/shop.html')

def contact(request):
    return render(request, 'store/contact.html')

def cart(request):
    return render(request, 'store/cart.html')

def checkout(request):
    return render(request, 'store/checkout.html')

def shop_details(request, slug):
    return render(request, 'store/shop_details.html')

def profile(request):
    return render(request, 'store/profile.html')


# ============================================================
# LOGIN VIEW
# ============================================================
def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('store:index')
        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'store/login.html')


# ============================================================
# SIGNUP VIEW
# ============================================================
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('store:index')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        username   = request.POST.get('username')
        email      = request.POST.get('email')
        phone      = request.POST.get('phone')
        password1  = request.POST.get('password1')
        password2  = request.POST.get('password2')

        # Check passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('store:signup')

        # Check username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('store:signup')

        # Check email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('store:signup')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        # Create profile for user
        Profile.objects.create(user=user, phone=phone)

        messages.success(request, 'Account created! Please login.')
        return redirect('store:login')

    return render(request, 'store/signup.html')


# ============================================================
# LOGOUT VIEW
# ============================================================
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('store:index')



def shop(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Filter by category
    selected_category = request.GET.get('category')
    if selected_category:
        products = products.filter(category__slug=selected_category)

    # Filter by price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'total_products': Product.objects.count(),
        'search_query': search_query or '',
        'min_price': min_price or '',
        'max_price': max_price or '',
    }
    return render(request, 'store/shop.html', context)




def shop_details(request, slug):
    # Get product or show 404 if not found
    product = get_object_or_404(Product, slug=slug)

    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/shop_details.html', context)


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Check if already in cart
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
    )

    if not created:
        # Already in cart — increase quantity
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity in cart!')
    else:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'{product.name} added to cart!')

    return redirect('store:cart')


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate totals
    subtotal = sum(item.get_total() for item in cart_items)
    shipping = 0 if subtotal >= 500 else 50
    total = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


@login_required
def update_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    action = request.POST.get('action')

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('store:cart')


@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart!')
    return redirect('store:cart')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, 'Your cart is empty!')
        return redirect('store:cart')

    subtotal = sum(item.get_total() for item in cart_items)
    shipping = 0 if subtotal >= 500 else 50
    total = subtotal + shipping

    if request.method == 'POST':
        from .models import BillingAddress, Order, OrderItem

        # Save billing address
        billing = BillingAddress.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pin_code=request.POST.get('pin_code'),
            notes=request.POST.get('notes'),
        )

        # Create order
        order = Order.objects.create(
            user=request.user,
            billing_address=billing,
            total_amount=total,
            status='pending'
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.get_price()
            )

        # Clear cart after order
        cart_items.delete()

        messages.success(
            request,
            f'Order #{order.id} placed successfully!'
        )
        return redirect('store:index')

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': total,
    }
    return render(request, 'store/checkout.html', context)


def contact(request):
    if request.method == 'POST':
        messages.success(
            request,
            'Message sent successfully! We will contact you soon.'
        )
        return redirect('store:contact')
    return render(request, 'store/contact.html')


@login_required
def profile(request):
    from .models import Order
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    cart_count = Cart.objects.filter(user=request.user).count()

    context = {
        'orders': orders,
        'cart_count': cart_count,
    }
    return render(request, 'store/profile.html', context)