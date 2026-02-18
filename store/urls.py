from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.user_signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('product/<slug:slug>/', views.shop_details, name='shop_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # ✅ New Cart URLs
    path('update-cart/<int:cart_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
]