from django.urls import path
from . import views

app_name = 'achironet_admin'

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("sellers/", views.sellers, name="sellers"),
    path("seller_claims/", views.seller_revenue_claims, name="seller_claims"),
    path("seller_claims/claim/<int:pk>/", views.ClaimPaidUpdateView.as_view(), name="claim_update"),
    path("customers/", views.buyers, name="customers"),
    path("products/", views.products, name="products"),
    path('view/product/<int:pk>/', views.ProductDetailView.as_view(), name="product_view"),
    path('view/product/<int:pk>/edit',
         views.ProductUpdateView.as_view(), name="product_edit"),
    path('add-product-images/<int:pk>/', views.add_product_images, name="add_product_images"),
    path('edit-product-images/<int:pk>/', views.edit_product_images, name="edit_product_images"),
    path('products/upload-image/', views.upload_image, name="upload_images"),
    path('products/delete-images/', views.delete_images, name="delete_images"),
    path("orders/", views.orders, name="orders"),
    path("orders/ship-order/", views.ship_order, name="ship_order"),
     path("orders/change-items/", views.change_items, name="change_items"),
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
    path("agent-commission-claims/", views.agent_commission_claims, name="agent_claims"),
    path("agent-commission-claims/claim/<int:pk>/", views.AgentClaimPaidUpdateView.as_view(), name="agent_claim_update")
]
