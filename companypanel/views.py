from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CompanyProfileForm ,  JobForm
from adminpanel.models import CompanyProfile , Job , ApplicationNotification , CompleteProfile
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout 

# Create your views here.

def company_home(request):
    logged_user = request.user
    company = get_object_or_404(CompanyProfile, user=request.user)  # Ensure company is being fetched correctly

    context = {
        'logged_user': logged_user,
        'company' : company
        
        
}
    return render(request, 'companypanel/company_home.html' , context)


@login_required
def add_company_profile(request):
    # Check if the user already has a company profile
    if CompanyProfile.objects.filter(user=request.user).exists():
        messages.error(request, "You already have a company profile. You can edit your profile instead.")
        return redirect('edit_company_profile')  # Redirect to the edit profile page

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES)
        if form.is_valid():
            company_profile = form.save(commit=False)
            company_profile.user = request.user  # Link the profile to the logged-in user
            try:
                company_profile.save()
                return redirect('view_company_profile')  # Redirect to the company profile page after successful creation
            except IntegrityError:
                messages.error(request, "You already have a company profile.")
                return redirect('edit_company_profile')  # Redirect to edit profile if a profile exists
    else:
        form = CompanyProfileForm()
    
    return render(request, 'companypanel/add_company_profile.html', {'form': form})


@login_required
def view_company_profile(request):
    company = get_object_or_404(CompanyProfile, user=request.user)  # Ensure company is being fetched correctly
    return render(request, 'companypanel/view_company_profile.html', {'company': company})


@login_required
def edit_company_profile(request):
    profile = get_object_or_404(CompanyProfile, user=request.user)
    
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_company_profile')  # Redirect to the profile view after editing
    else:
        form = CompanyProfileForm(instance=profile)
    
    return render(request, 'companypanel/edit_company_profile.html', {'form': form})



# Add Job
@login_required
def add_job(request):
    logged_user = request.user
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.companyprofile  # Assuming the user is linked to a company profile
            job.save()
            return redirect('view_job', pk=job.pk)
    else:
        form = JobForm()
    return render(request, 'companypanel/job_form.html', {'form': form , 'logged_user': logged_user})

# View Job
@login_required
def view_job(request, pk):
    logged_user = request.user
    job = get_object_or_404(Job, pk=pk, company=request.user.companyprofile)
    return render(request, 'companypanel/view_job.html', {'job': job , 'logged_user': logged_user})

# Edit Job
@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user.companyprofile)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('view_job', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'companypanel/job_form.html', {'form': form})


@login_required
def job_list(request):
    # Get the logged-in user’s company profile
    company = request.user.companyprofile
    
    # Filter jobs by the logged-in company's profile
    jobs = Job.objects.filter(company=company)
    
    return render(request, 'companypanel/job_list.html', {'jobs': jobs})



def application_notifications(request):
    # Get the current user's notifications
    company_notifications = ApplicationNotification.objects.filter(company_user=request.user)

    return render(request, 'companypanel/application_notification.html', {
        'company_notifications': company_notifications
    })




def mark_application(request, notification_id, action):
    # Retrieve the notification by ID
    notification = get_object_or_404(ApplicationNotification, id=notification_id)

    if action == 'selected':
        job = notification.job
        if job.openings > 0:
            job.openings -= 1
            job.save()

            # Get the company name
            company_name = job.company.company_name

            # Create a notification for the applicant
            notification_message = f"You are selected for the first round mock section by {company_name}. Check your mail for further details."

            # Send notification to the applicant's user panel
            ApplicationNotification.objects.create(
                job=job,
                company_user=notification.company_user,
                applicant=notification.applicant,
                message=notification_message
            )

            # Delete the original notification after marking as selected
            notification.delete()

            messages.success(request, 'The applicant has been notified in their user panel.')

        else:
            messages.error(request, 'No more job openings available for this position.')
    elif action == 'deleted':
        notification.delete()
        messages.success(request, 'The notification has been deleted.')

    return redirect('application_notifications')  # Adjust the URL name to the correct one





def delete_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(ApplicationNotification, id=notification_id, company_user=request.user)
        notification.delete()
        return redirect('application_notifications')  # Redirect back to the notification page
    


def company_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')