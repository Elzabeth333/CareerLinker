from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminpanel.models import CompanyProfile , User , Job , CompleteProfile , Notification
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse

# Create your views here.
def admin_home(request):
    # Get total counts
    total_companies = CompanyProfile.objects.count()
    total_users = User.objects.filter(is_superuser=False, is_staff=False).count()
    total_jobs = Job.objects.count()

    # Get lists
    company_list = CompanyProfile.objects.all().order_by('-created_at')[:5]  # Latest 5 companies
    job_list = Job.objects.all().order_by('-posted_at')[:5]  # Latest 5 jobs
    user_list = User.objects.filter(is_superuser=False, is_staff=False).order_by('-date_joined')[:5]


    return render(request, 'adminpanel/admin_home.html', {
        'total_companies': total_companies,
        'total_users': total_users,
        'total_jobs': total_jobs,
        'company_list': company_list,
        'job_list': job_list,
        'user_list': user_list
    })




def company_detail(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    return render(request, 'adminpanel/company_detail.html', {
        'company': company
    })


def applicant_user_list(request):
    # Fetch users whose 'is_hidden' status is managed by CompleteProfile
    applicants = CompleteProfile.objects.filter(user__is_superuser=False, user__is_staff=False)
    return render(request, 'adminpanel/applicant_user_list.html', {'applicants': applicants})

@login_required
def hide_applicant(request, applicant_id):
    applicant = get_object_or_404(CompleteProfile, id=applicant_id)
    applicant.user.is_active = False  # Hide by setting is_active to False
    applicant.user.save()
    messages.success(request, 'Applicant successfully hidden.')
    return redirect('applicant_user_list')

@login_required
def unhide_applicant(request, applicant_id):
    applicant = get_object_or_404(CompleteProfile, id=applicant_id)
    applicant.user.is_active = True  # Unhide by setting is_active to True
    applicant.user.save()
    messages.success(request, 'Applicant successfully unhidden.')
    return redirect('applicant_user_list')

@login_required
def active_users_list(request):
    users = User.objects.filter(is_active=True)  # Get all active users
    return render(request, 'adminpanel/unhide_user.html', {'users': users})

@login_required
def hidden_users_list(request):
    hidden_users = User.objects.filter(is_active=False)  # Get all hidden users
    return render(request, 'adminpanel/hide_user.html', {'hidden_users': hidden_users})


def view_applicant(request, id):
    applicant = CompleteProfile.objects.get(id=id)
    return render(request, 'adminpanel/view_applicant.html', {'applicant': applicant})


def company_list(request):
    companies = CompanyProfile.objects.all()

    return render(request, 'adminpanel/company_list.html', {
        'companies': companies
    })

def toggle_company_status(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    
    # Toggle the is_active field (assuming there's an is_active field in CompanyProfile)
    company.is_active = not company.is_active
    company.save()

    # Provide appropriate message depending on the new status
    if company.is_active:
        messages.success(request, f"{company.company_name} has been activated.")
    else:
        messages.success(request, f"{company.company_name} has been deactivated.")

    return redirect('company_list')


# View to list all available jobs
@login_required
def available_jobs_list(request):
    jobs = Job.objects.filter(is_active=True, selected_candidates__lt=F('openings'))  # Filter jobs with openings
    return render(request, 'jobs/available_jobs.html', {'jobs': jobs})

# View to list hired jobs
@login_required
def hired_jobs_list(request):
    jobs = Job.objects.filter(is_active=True, selected_candidates__gte=F('openings'))  # Filter jobs where hiring is complete
    return render(request, 'jobs/hired_jobs.html', {'jobs': jobs})

@login_required
def admin_notifications(request):
    notifications = Notification.objects.all().order_by('-created_at')  # Fetch all notifications
    return render(request, 'adminpanel/notifications.html', {'notifications': notifications})    




def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')