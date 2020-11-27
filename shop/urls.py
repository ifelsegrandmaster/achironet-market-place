from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    url(r'^shop/search/$', views.search_products, name='search'),
    path('<slug:category_slug>/', views.product_list,
         name='product_list_by_category'),
    path('view/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('shop/contact/', views.contact, name="contact"),
    path('shop/sell/', views.sell_online, name="sell_online"),
    path('shop/publishing/products/',
         views.publish_product, name="publish_products"),
    path('shop/thanks/', views.thanks, name='thanks')
]
