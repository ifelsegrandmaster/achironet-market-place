"""config URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/', include('achironet_admin.urls',
                                     namespace='achironet_admin')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('order/', include('order.urls', namespace='order')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    path('', include('shop.urls', namespace='shop')),
    path('users/', include('users.urls'), name="users"),
    path('sell/', include('sell.urls', namespace='sell')),
    path('plugins/summernote/', include('django_summernote.urls')),
    path('accounts/login', CustomLoginView.as_view(), name="account_login"),
    path('accounts/register', CustomSignupView.as_view(), name="account_signup"),
    path('accounts/password/reset', CustomPasswordResetView.as_view(),
         name="account_reset_password"),
    path('accounts/logout', CustomLogoutView.as_view(), name="account_logout")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
