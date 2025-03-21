from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = "home"),
    path('register/', views.register, name="register"),
    path('register_form/', views.register_form, name="register_form"),
    path('login_form/', views.login_form, name='login_form'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_user, name='logout')
]
