from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('register/', views.register, name="register"),
    path('register_form/', views.register_form, name="register_form"),
    path('login_form/', views.login_form, name='login_form'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_user, name='logout'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('register-category', views.register_category, name="register_category"),
    path('add-product/', views.add_product, name='add_product'),
    path('update_product/', views.update_product, name="update_product"),
    path('delete_product/', views.delete_product, name = 'delete_product'),
    path('update_category/', views.update_category, name = "update_category"),
    path('delete_category/', views.delete_category, name='delete_category')
]
