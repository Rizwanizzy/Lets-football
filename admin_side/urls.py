from django.urls import path
from . import views

urlpatterns = [

    path('admin_home', views.admin_home , name='admin_home'),
    path('round_1', views.round_1 , name='round_1'),
    path('update_match/<int:id>', views.update_match , name='update_match'),
    path('semifinals', views.semifinals , name='semifinals'),
    path('finals', views.finals , name='finals'),
]
