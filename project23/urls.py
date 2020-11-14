"""project23 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app23 import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic import View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show, name='Home'),
    path('login/', views.login, name='login'),
    path('logincheck/', views.logincheck, name='logincheck'),
    path('logout/', views.logout, name='logout'),
    path('logined/', views.logined, name='logined'),
    path('get_product/', views.get_product, name='get_product'),
    path('views_product/', views.view_product, name='views_product'),
    path('cart_added/', views.cart_added, name='cart_added'),
    path('cart_items/', views.cart_items, name='cart_items'),
    path('remove_cart/', views.remove_cart, name='remove_cart'),
    path('user_login/', views.user_login, name='user_login'),
    path('register_user/', views.register_user, name='register_user'),
    path('registered_user/', views.registered_user, name='registered_user'),
    path('user_logined/', views.user_logined, name='user_logined'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('buy_product/', views.buy_product, name='buy_product'),
    path('UserCarts/', views.UserCarts.as_view(), name='UserCarts'),
    path('confirm_bill/', views.confirm_bill, name='confirm_bill'),
    path('open_cart/', views.open_cart, name='open_cart'),
    path('UserBills/', views.UserBills, name='UserBills'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
