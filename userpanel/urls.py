from django.urls import  path
from .views import userhome , add_profile , all_companies , jobs_by_company , search_jobs , view_profile , recommended_jobs ,  all_jobs , user_notifications , edit_profile , add_language_proficiency , user_logout , job_detail , apply_for_job

urlpatterns = [
    path('', userhome , name= 'userhome'),
    path('add_profile/', add_profile, name='add_profile'),
    path('view_profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/language/add/', add_language_proficiency, name='add_language_proficiency'),
    path('user_logoutt/', user_logout, name='user_logout'),  # URL for logout
    path('recommended-jobs/', recommended_jobs, name='recommended_jobs'),
    path('job_detail/<int:pk>/', job_detail, name='job_detail'),
    path('apply/<int:job_id>/', apply_for_job, name='apply_for_job'),
    path('usernotifications/', user_notifications, name='user_notifications'),
    path('all_jobs/', all_jobs, name='all_jobs'),
    path('all_companies/', all_companies, name='all_companies'),
    path('company/<int:company_id>/jobs/', jobs_by_company, name='jobs_by_company'),
    path('search_jobs/', search_jobs, name='search_jobs'),
   
]