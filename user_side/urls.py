from django.urls import path
from . import views

urlpatterns = [

    path('home', views.home , name='home'),
    path('squad', views.squad , name='squad'),
    path('standings', views.standings , name='standings'),
]
