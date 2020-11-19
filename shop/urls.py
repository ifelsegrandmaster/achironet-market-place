from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/about/', views.about, name="about"),
    path('shop/contact/', views.contact, name="contact"),
    path('shop/sell/', views.sell_online, name="sell_online"),
    path('shop/publishing/products/',
         views.publish_product, name="publish_products")
]
