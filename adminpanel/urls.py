from django.urls import  path
from .views import admin_home , admin_logout , company_detail , company_list , active_users_list , admin_notifications , hidden_users_list , hired_jobs_list , available_jobs_list , hide_applicant , unhide_applicant , toggle_company_status , applicant_user_list , view_applicant

urlpatterns = [
    path('',admin_home , name='admin_home'),
    path('company_list/', company_list, name='company_list'),
    path('toggle_company_status/<int:company_id>/', toggle_company_status, name='toggle_company_status'),
    path('company_detail/<int:company_id>/', company_detail, name='company_detail'),  # New view for company details
    path('applicants/', applicant_user_list, name='applicant_user_list'),
    path('applicant/hide/<int:applicant_id>/', hide_applicant , name='hide_applicant'),  # Hide applicant by ID
    path('applicant/unhide/<int:applicant_id>/', unhide_applicant, name='unhide_applicant'),  # Unhide applicant by ID
    path('applicants/', applicant_user_list, name='applicant_user_list'),  # List of all applicants
    path('applicant/<int:id>/', view_applicant, name='view_applicant'),  # Viewing individual applicants by ID
    path('active-users/', active_users_list, name='active_users_list'),  # List of active users
    path('hidden-users/', hidden_users_list, name='hidden_users_list'),  # List of hidden users
    path('available-jobs/', available_jobs_list, name='available_jobs_list'),
    path('hired-jobs/', hired_jobs_list, name='hired_jobs_list'),
    path('notifications/', admin_notifications, name='admin_notifications'),
    path('logout/', admin_logout, name='admin_logout'),

]