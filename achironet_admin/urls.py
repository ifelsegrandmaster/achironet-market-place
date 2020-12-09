from django.urls import path
from . import views

app_name = 'achironet_admin'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sellers/", views.sellers, name="sellers"),
    path("customers/", views.buyers, name="customers"),
    path("orders/", views.orders, name="orders"),
     path("orders/change-items/", views.orders, name="orders"),
    path("email-newsletters/", views.email_newsletters, name="email_newsletters"),
    path("request-testmonials/", views.request_testmonials,
         name="request_testmonials"),
    path("seller-testmonials/", views.seller_testmonials,
         name="seller_testmonials"),
    path("page-not-found/", views.http_404_not_available,
         name="http_404_not_available"),
    path("mail-sellers/", views.mail_sellers, name="mail_sellers"),
    path("delete-testmonial/", views.delete_testmonial, name="delete_testmonial"),
    path("approve-testmonial/", views.approve_testmonial,
         name="approve_testmonial"),
    path("create-newsletter/", views.create_email_newsletter,
         name='create_newsletter'),
    path("edit-newsletter/<pk>/",
         views.EditEmailnewsletter.as_view(), name="edit_newsletter"),
    path("delete-newsletter/", views.delete_newsletter,
         name='delete_newsletter'),
    path("orders/view/<int:pk>/", views.OrderDetailView.as_view(),
         name='order_view'),
]
