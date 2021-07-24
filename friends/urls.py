from django.urls import path
from . import views

urlpatterns = [
    path('', views.friends),
    path('newfriend', views.newfriend),
    path('delete', views.delete),
    path('user/<int:id>', views.profile)
]
