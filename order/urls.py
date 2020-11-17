from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('view/<pk>/', views.OrderDetailView.as_view(), name="order_view"),
    path('<pk>/payment/', views.PaymentView.as_view(), name="payment"),
    path('404-not-found/', views.http_404_not_found, name="http-404-not-found")
]
