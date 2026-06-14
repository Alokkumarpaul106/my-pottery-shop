from django.urls import path
from .import views
app_name='backend'



urlpatterns = [
path('login/',views.login_view,name='login'),
path('register/',views.register_view,name='register'),
path('logout/',views.logout_view,name='logout'),
path('profile/',views.profile,name='profile'),

path('', views.home, name='home'),
path('category',views.category,name='category'),
path('new_arrival',views.new_arrival,name='new_arrival'),
path('products/',views.product_list,name='product_list'),
path('product/detail/<slug:slug>/',views.product_detail,name='product_detail'),
path('category/<slug:slug>/', views.category_products, name='category_products'),


path('cart/', views.cart_list, name='cart_list'),
path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
path('cart/remove/<int:cart_item_id>/', views.cart_remove, name='cart_remove'),
path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),

path('checkout/', views.checkout, name='checkout'),
path('order/process/<int:order_id>/',views.order_process,name='order_process'),
# path('payment/process/<int:order_id>/', views.payment_process, name='payment_process'),
# path('payment/success/', views.payment_success, name='payment_success'),
# path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
# path('payment/error/', views.payment_error, name='payment_error'),
path('about_us/',views.about,name='about'),
path('contact/',views.contact, name='contact'),
path('returns_exchanges/',views.returns,name='returns'),


]