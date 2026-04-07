from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('home/<str:category>/', views.home_with_category, name='home_with_category'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create_product/', views.create_product, name='create_product'),
    path('update_product/<int:pk>/', views.update_product, name='update_product'),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('shop/', views.shop, name='shop'),
    path('discounts/', views.discounts, name='discounts'),
    path('contact/', views.contact, name='contact'),
    path('goals/', views.goals, name='goals'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),  # <--- ky është emri
    path('cart/', views.cart_view, name='cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:pk>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:pk>/', views.decrease_quantity, name='decrease_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('update_order_status/<int:order_id>/<str:new_status>/', views.update_order_status, name='update_order_status'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('success/', views.success, name='success'),
]

