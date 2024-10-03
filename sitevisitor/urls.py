from django.urls import  path
from .views import home ,  user_login , admin_login , user_register , forgot_password , company_register , company_login

urlpatterns = [
    path('',home , name='home'),
    path('user_register/',user_register, name='user_register'),
    path('user_login/', user_login , name='user_login'),
    path('admin_login/', admin_login , name='admin_login'),
    path('forgot_password/', forgot_password , name='forgot_password'),
    path('admin_login/', admin_login, name='admin_login'),
    path('company_register/', company_register, name='company_register'),
    path('company_login/', company_login, name='company_login'),

]