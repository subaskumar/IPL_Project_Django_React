"""Electronics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from electroApp import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home , name="home"),
    
    path('autofilAddress/', views.Autofill_address , name="addressFill"),
    path('verifyPhone/',views.ValidatePhoneSendOTP,name="verifyPhone"),
    path('verifyOTP/',views.VerifyOTP,name="verifyotp"),
    path('UserLogin/',views.login_view,name="Login"),
    path('UserLogout/',views.logout_view,name="Logout"),
    path('UserProfile/<int:id>',views.UserProfile,name="profile"),
    path('UserAddress/',views.Cutomer_address,name="customer_address"),
    path('cart/', views.cart , name="Cart"),
    path('myOrder/', views.Orders , name="orders"),
    path('add_to_cart/', views.add_to_cart , name="add_to_cart"),
    path('remove_to_cart/<int:id>', views.remove_to_cart , name="remove_to_cart"),
    path('Plus_minus_quantity/', views.update_quantity , name="update_quantity"),
    path('CheckOut/', views.checkOut , name="checkout"),
    path(' paymentDone/confirmOrder', views.paymentDone , name="paymentDone"),
    path('mobile/<slug:data>', views.mobile_view , name="mobile"),
    path('ProductDetails/<int:id>',views.product_detail_view,name="Product_Detail"),
    path('account/password_change/', views.password_change ,name='password_change'),





] #   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)