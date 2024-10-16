from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import CompanyProfileForm ,  JobForm
from adminpanel.models import CompanyProfile , NotificationMessage , Job , ApplicationNotification , CompleteProfile , JobApplication , Notification
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.views import View
from django.contrib.auth import authenticate, login, logout 

# Create your views here.

def company_home(request):
    logged_user = request.user
    if not CompanyProfile.objects.filter(user=request.user).exists():
        # Redirect to add profile page if no company profile exists
        return redirect('add_company_profile')
    
    company = CompanyProfile.objects.get(user=request.user)  # Profile exists, now get it
    job = Job.objects.filter(company__user=request.user).first()
    
    # Make sure to check if job exists
    if job is None:
        return render(request, 'companypanel/company_home.html', {
            'error': 'No jobs available for this company.'
        })

    context = {
        'logged_user': logged_user,
        'company' : company,
        'job':job,
        
        
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

                # Create a notification for the admin that a new company profile has been added
                Notification.objects.create(
                    notification_type='company',
                    content_object_id=company_profile.id,
                    message=f"New company {company_profile.company_name} added."
                )

                return redirect('view_company_profile')  # Redirect to the company profile page after successful creation
            except IntegrityError:
                messages.error(request, "You already have a company profile.")
                return redirect('edit_company_profile')  # Redirect to edit profile if a profile exists
    else:
        form = CompanyProfileForm()

    return render(request, 'companypanel/add_company_profile.html', {'form': form})




# @login_required
# def add_company_profile(request):
#     company = get_object_or_404(CompanyProfile, user=request.user) 
#     # Check if the user already has a company profile
#     if CompanyProfile.objects.filter(user=request.user).exists():
#         messages.error(request, "You already have a company profile. You can edit your profile instead.")
#         return redirect('edit_company_profile')  # Redirect to the edit profile page

#     if request.method == 'POST':
#         form = CompanyProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             company_profile = form.save(commit=False)
#             company_profile.user = request.user  # Link the profile to the logged-in user
#             try:
#                 company_profile.save()
#                 return redirect('view_company_profile')  # Redirect to the company profile page after successful creation
#             except IntegrityError:
#                 messages.error(request, "You already have a company profile.")
#                 return redirect('edit_company_profile')  # Redirect to edit profile if a profile exists
#     else:
#         form = CompanyProfileForm()
    
#     return render(request, 'companypanel/add_company_profile.html', {'form': form , 'company':company})


@login_required
def view_company_profile(request):
    company = get_object_or_404(CompanyProfile, user=request.user)  # Ensure company is being fetched correctly
    return render(request, 'companypanel/view_company_profile.html', {'company': company})


@login_required
def edit_company_profile(request):
    company = get_object_or_404(CompanyProfile, user=request.user) 
    profile = get_object_or_404(CompanyProfile, user=request.user)
    
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_company_profile')  # Redirect to the profile view after editing
    else:
        form = CompanyProfileForm(instance=profile)
    
    return render(request, 'companypanel/edit_company_profile.html', {'form': form , 'company':company})


@login_required
def add_job(request):
    logged_user = request.user
    company = get_object_or_404(CompanyProfile, user=request.user)  # Get the company profile linked to the user

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.companyprofile  # Link the job to the user's company profile
            job.save()

            # Create a notification for the admin that a new job has been added
            Notification.objects.create(
                notification_type='job',
                content_object_id=job.id,
                message=f"New job '{job.title}' added at {job.company.company_name}."
            )

            return redirect('view_job', pk=job.pk)  # Redirect to the view job page after adding
    else:
        form = JobForm()

    return render(request, 'companypanel/job_form.html', {'form': form, 'logged_user': logged_user, 'company': company})




# # Add Job
# @login_required
# def add_job(request):
#     logged_user = request.user
#     company = get_object_or_404(CompanyProfile, user=request.user) 
#     if request.method == 'POST':
#         form = JobForm(request.POST)
#         if form.is_valid():
#             job = form.save(commit=False)
#             job.company = request.user.companyprofile  # Assuming the user is linked to a company profile
#             job.save()
#             return redirect('view_job', pk=job.pk)
#     else:
#         form = JobForm()
#     return render(request, 'companypanel/job_form.html', {'form': form , 'logged_user': logged_user , 'company':company})

# View Job
@login_required
def view_job(request, pk):
    logged_user = request.user
    company = get_object_or_404(CompanyProfile, user=request.user) 
    job = get_object_or_404(Job, pk=pk, company=request.user.companyprofile)
    return render(request, 'companypanel/view_job.html', {'job': job , 'logged_user': logged_user , 'company':company})

# Edit Job
@login_required
def edit_job(request, pk):
    company = get_object_or_404(CompanyProfile, user=request.user) 
    job = get_object_or_404(Job, pk=pk, company=request.user.companyprofile)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('view_job', pk=job.pk)
    else:
        form = JobForm(instance=job)
    return render(request, 'companypanel/job_form.html', {'form': form , 'company':company})


@login_required
def job_list(request):
    # Get the logged-in user’s company profile
    company_profile = get_object_or_404(CompanyProfile, user=request.user) 
    company = request.user.companyprofile
    
    # Filter jobs by the logged-in company's profile
    jobs = Job.objects.filter(company=company)
    
    return render(request, 'companypanel/job_list.html', {'jobs': jobs , 'company_profile':company_profile})



@login_required
def application_notifications(request):
    company = get_object_or_404(CompanyProfile, user=request.user)  # Ensure company is being fetched correctly
    job = Job.objects.filter(company__user=request.user).first()

    if not job:
        messages.error(request, 'No job found for this company.')
        return redirect('company_home')  # Redirect if no job is found

    # Filter notifications where the current user is the receiver
    company_notifications = ApplicationNotification.objects.filter(
        company_user=request.user
    ).order_by('-created_at')

    return render(request, 'companypanel/application_notification.html', {
        'company_notifications': company_notifications,
        'company': company,
        'job': job,
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



class SelectedCandidatesView(View):
    template_name = 'companypanel/selected_candidates.html'  # Path to your template

    def get(self, request, job_id):
        # Get the job object
        job = get_object_or_404(Job, id=job_id)

        # Fetch the selected candidates for this job
        selected_candidates = JobApplication.objects.filter(job=job, is_selected=True)

        return render(request, self.template_name, {
            'job': job,
            'selected_candidates': selected_candidates,
        })



@login_required
@transaction.atomic  # Ensure the actions happen together or roll back
def reject_application(request, notification_id):
    notification = get_object_or_404(ApplicationNotification, id=notification_id)
    job = notification.job
    company_name = job.company.company_name
    applicant = notification.applicant

    # Mark the applicant's application as rejected
    job_application = JobApplication.objects.filter(user=applicant, job=job).first()
    if job_application:
        # Set the application status to rejected (assuming `status` field)
        job_application.status = 'rejected'
        job_application.save()

        # Send a rejection notification to the applicant
        NotificationMessage.objects.create(
            sender=request.user,
            receiver=applicant,  # The applicant receives the notification
            subject=f'Application for {job.title} Rejected',
            body=f'Your application for the {job.title} position at {company_name} has been rejected.',
        )

        # Optionally: Delete the original notification
        notification.delete()

        messages.success(request, f'The applicant {applicant.username} has been rejected and notified.')
    else:
        messages.error(request, 'Job application for this user does not exist.')
        return redirect('application_notifications')

    # Redirect back to the notifications page
    return redirect('application_notifications')



def mark_as_selected(job_application):
    job_application.is_selected = True
    job_application.save()


class SelectedCandidatesView(View):
    template_name = 'companypanel/selected_candidates.html'

    def get(self, request, job_id):
        job = get_object_or_404(Job, id=job_id)
        selected_candidates = JobApplication.objects.filter(job=job, is_selected=True)
        
        # Group selected candidates by job
        job_selected_candidates = {
            job: selected_candidates,
        }

        return render(request, self.template_name, {
            'job_selected_candidates': job_selected_candidates,
        })


def delete_notification(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(ApplicationNotification, id=notification_id, company_user=request.user)
        notification.delete()
        return redirect('application_notifications')  # Redirect back to the notification page





def company_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')