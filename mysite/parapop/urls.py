from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='homepage'),
    #path('register', views.register, name='User-registration'),
]
