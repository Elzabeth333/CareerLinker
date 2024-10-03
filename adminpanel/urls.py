from django.urls import  path
from .views import admin_home , admin_logout , company_detail , company_list

urlpatterns = [
    path('',admin_home , name='admin_home'),
    path('company_detail/', company_detail, name='company_detail'),
    path('company_list/', company_list, name='company_list'),
    path('logout/', admin_logout, name='admin_logout'),

]