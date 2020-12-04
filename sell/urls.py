from django.urls import path
from . import views

app_name = 'sell'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('revenue/', views.revenue, name='revenue'),
    path('revenue/<int:pk>/', views.RevenueDetailView.as_view(), name='revenue_view'),
    path("fetch-revenue-data/", views.get_revenue_data, name="fetch_revenue_data"),
    path('orders/', views.orders, name='orders'),
    path('view/order/<int:pk>/', views.OrderDetailView.as_view(), name="order_view"),
    path('404-not-found/', views.http_404_not_found, name="http-404-not-found"),
    path('products/', views.products, name='products'),
    path('products/create/', views.ProductCreateView.as_view(),
         name="product_create"),
    path('add-product-images/<int:pk>/', views.add_product_images, name="add_product_images"),
    path('products/upload-image/', views.upload_image, name="upload_images"),
    path('products/delete-images/', views.delete_images, name="delete_images"),
    path('products/<pk>/create-overview/',
         views.OverviewCreateView.as_view(), name="create_overview"),
    path('products/update-overview/<int:pk>/',
         views.OverviewUpdateView.as_view(), name="update_overview"),
    path('products/<pk>/create-specification/',
         views.create_specification, name="create_specification"),
    path('products/update-specification/<int:pk>/',
         views.update_specification, name="update_specification"),
    path('view/product/<int:pk>/', views.ProductDetailView.as_view(), name="product_view"),
    path('view/product/<int:pk>/edit',
         views.ProductUpdateView.as_view(), name="product_edit")
]
