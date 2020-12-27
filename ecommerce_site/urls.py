"""config URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from shop.views import *
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap, Sitemap
from shop.models import Product

info_dict = {
    "queryset": Product.objects.all(),
    "date_field": "created"
}


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['account_login', 'account_logout', 'shop:product_list', 'shop:sell_online']

    def location(self, item):
        return reverse(item)


sitemaps = {
    "shop": GenericSitemap(info_dict, priority=0.6),
    "static": StaticViewSitemap
}

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
    path('accounts/logout', CustomLogoutView.as_view(), name="account_logout"),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
