from django.urls import path
from . import views
app_name = 'users'
urlpatterns = [
    path("profile/<pk>/", views.ProfileView.as_view(), name="profile"),
    path("create-profile/", views.create_user_profile, name="create-profile"),
    path("edit-profile/<pk>/", views.UpdateProfileView.as_view(), name="edit-profile"),
    path("create-seller-profile", views.create_seller_profile,
         name="create-seller-profile"),
    path("seller-profile/<pk>/",
         views.SellerProfileView.as_view(), name="seller-profile"),
    path("edit-seller-profile/<pk>/",
         views.UpdateSellerProfileView.as_view(), name="edit-seller-profile"),
    path("product-review/<pk>/", views.product_review,
         name="create_or_edit_product_review"),
    path('404-not-found/', views.http_404_not_found, name="http_404_not_found"),
]
