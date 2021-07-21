from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.registerForm),
    path('new', views.register),
    path('logout', views.logout),
    path('logged', views.logged)
]
