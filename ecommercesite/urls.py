"""
URL configuration for ecommercesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ecommerceapp.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('index/',index,name='index'),
    path('about/',about,name='about'),
    path('main/',main_index,name='main'),
    path('admin_login/',adminLogin,name='admin_login'),
    path('adminhome/', adminHome, name="adminhome"),
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),
    path('add-product/', add_product, name='add_product'),
    path('view-product/', view_product, name='view_product'),
    path('edit-product/<int:pid>/', edit_product, name="edit_product"),
    path('delete-product/<int:pid>/', delete_product, name="delete_product"),
    path('registration/', registration, name="registration"),
    path('userlogin/', userlogin, name="userlogin"),
    path('logout/', logoutuser, name="logout"),
    path('profile/', profile, name="profile"),
    path('change-password/', change_password, name="change_password"),
    path('user-product/<int:pid>/', user_product, name="user_product"),
    path('product-detail/<int:pid>/', product_detail, name="product_detail"),
    path('add-to-cart/<int:pid>/', addToCart, name="addToCart"),
    path('cart/', cart, name="cart"),
    path('incredecre/<int:pid>/', incredecre, name="incredecre"),
    path('deletecart/<int:pid>/', deletecart, name="deletecart"),
    path('booking/', booking, name="booking"),
    
    path('my-order/', myOrder, name="myorder"),
    path('user-order-track/<int:pid>/', user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', change_order_status, name="change_order_status"),
    path('payment/', payment, name="payment"), 
    path('manage-order/', manage_order, name="manage_order"), 
    path('delete-order/<int:pid>/', delete_order, name="delete_order"), 
    path('admin-order-track/<int:pid>/', admin_order_track, name="admin_order_track"),
    path('manage-user/', manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', delete_user, name="delete_user"),
    path('admin-change-password/',admin_change_password, name="admin_change_password"),
     path('bookings/', booking_list, name='booking_list'),
     path('user-product-summary/', user_product_summary, name='user_product_summary'),
     path('user-product-summary2/', user_product_summary2, name='user_product_summary2'),
     path('product-orders/', get_product_orders, name='product_orders'),
     path('product-quantity-summary/', product_quantity_summary, name='product_quantity_summary'),
     path('weekly-orders-q1-2024/', weekly_orders_q1_2024, name='weekly_orders_q1_2024'),
     path('product-sales/', product_sales_view, name='product_sales'),
      path('sold_product/', sold_product, name='sold_product'),
      path('unsold_product/', unsold_product, name='unsold_product'),
       path('query5/', query5, name='query5'),
       path('query6/', query6, name='query6'),
       path('query4/', query7, name='query7'),
        path('booking/<int:pk>/update/', update_booking, name='update_booking'),
        path('query2/',query2,name='query2'),
       
     


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
