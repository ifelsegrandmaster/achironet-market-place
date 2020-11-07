from django.urls import path
from . import views

app_name = 'sell'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('revenue/', views.revenue, name='revenue'),
    path('orders/', views.orders, name='orders'),
    path('products/', views.products, name='products'),
    path('view/order/<pk>/', views.OrderDetailView.as_view(), name="order_view"),
    path('404-not-found/', views.http_404_not_found, name="http-404-not-found"),
    path('view/product/<pk>/',views.ProductDetailView.as_view(), name="product_view"),
    path('view/product/<pk>/edit', views.ProductUpdateView.as_view(), name="product_edit"),
]