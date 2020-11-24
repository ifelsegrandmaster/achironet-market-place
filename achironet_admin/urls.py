from django.urls import path
from . import views

app_name = 'achironet_admin'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sellers/", views.sellers, name="sellers"),
    path("buyers/", views.buyers, name="buyers"),
    path("email-newsletters/", views.email_newsletters, name="email_newsletters"),
    path("request-testmonials/", views.request_testmonials,
         name="request_testmonials"),
    path("page-not-found/", views.http_404_not_available,
         name="http_404_not_available"),
    path("mail-sellers/", views.mail_sellers, name="mail_sellers")
]
