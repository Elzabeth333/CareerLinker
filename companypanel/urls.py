from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import company_home, add_job ,  edit_job ,  view_job , job_list , add_company_profile,  mark_application,  company_logout ,  view_company_profile, edit_company_profile , delete_notification , application_notifications

urlpatterns = [
    path('', company_home, name='company_home'),
    path('companyview_profile/', view_company_profile, name='view_company_profile'),
    path('companyedit_profile/', edit_company_profile, name='edit_company_profile'),
    path('companyadd_profile/', add_company_profile, name='add_company_profile'),
    path('jobs/add/', add_job, name='add_job'),
    path('jobs/<int:pk>/', view_job, name='view_job'),
    path('jobs/<int:pk>/edit/', edit_job, name='edit_job'),
    path('company/notifications/', application_notifications, name='application_notifications'),
    path('notifications/delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('job_list/', job_list, name='job_list'),
    path('logout/', company_logout, name='company_logout'),
    path('notifications/<int:notification_id>/<str:action>/', mark_application, name='mark_application'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
