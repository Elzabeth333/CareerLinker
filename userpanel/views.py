from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminpanel.models import Skill , Job ,  NotificationMessage , CompleteProfile , LanguageProficiency , ApplicationNotification , JobApplication , CompanyProfile
from .forms import CompleteProfileForm , CompleteProfileSkillForm , LanguageProficiencyForm 
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.contrib.auth import logout
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.html import format_html


@login_required
def userhome(request):
    logged_user = request.user
    try:
        # Try to get the user's CompleteProfile
        f_profile = CompleteProfile.objects.get(user=request.user)
    except CompleteProfile.DoesNotExist:
        # Redirect to a profile completion page or create a blank profile
        return redirect('add_profile')  # Assuming 'complete_profile' is a view for updating profiles
    
    profile = get_object_or_404(CompleteProfile, user=logged_user)

    # Get user's skills from the profile
    user_skills = profile.skills.all()

    # Prepare a Q object for jobs matching any of the user's skills
    query = Q()
    for skill in user_skills:
        query |= Q(key_skills__icontains=skill.name)

    # Fetch jobs matching any of the user's skills
    recommended_jobs = Job.objects.filter(query).distinct()

    # Get jobs the user has applied for
    applied_jobs = JobApplication.objects.filter(user=logged_user).values_list('job_id', flat=True)

    # Exclude the jobs the user has already applied for from the matched jobs
    matched_jobs = recommended_jobs.exclude(id__in=applied_jobs)

    # Fetch top companies (you can adjust the number or add filters)
    companies = CompanyProfile.objects.all()[:3]

    if request.method == 'POST':
        # Handle adding a new skill
        if 'add_skill' in request.POST:
            new_skill = request.POST.get('skill_name').strip()  # Get the new skill from input field
            if new_skill:  # Ensure it's not empty
                skill, created = Skill.objects.get_or_create(name=new_skill)
                profile.skills.add(skill)
            return redirect('userhome')  # Redirect to the same page

        # Handle deleting an existing skill
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('skill_id')
            skill_to_remove = Skill.objects.filter(id=skill_id).first()
            if skill_to_remove:
                profile.skills.remove(skill_to_remove)
            return redirect('userhome')

        # Save the profile first before handling the languages
        form = CompleteProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

        # Handle languages
        LanguageProficiency.objects.filter(profile=profile).delete()  # Clear existing languages

        # Identify the maximum language index dynamically
        language_count = max([int(key.split('_')[1]) for key in request.POST if key.startswith('language_')] or [0])

        for i in range(language_count + 1):
            language = request.POST.get(f'language_{i}')
            proficiency = request.POST.get(f'proficiency_{i}')
            read = request.POST.get(f'read_{i}', False)
            write = request.POST.get(f'write_{i}', False)
            speak = request.POST.get(f'speak_{i}', False)

            if language and proficiency:
                LanguageProficiency.objects.create(
                    profile=profile,
                    language=language,
                    proficiency=proficiency,
                    read=read == 'on',
                    write=write == 'on',
                    speak=speak == 'on'
                )

        return redirect('userhome')  # Redirect back to userhome after saving changes

    else:
        form = CompleteProfileForm(instance=profile)

    # Fetch the languages associated with the profile
    languages = LanguageProficiency.objects.filter(profile=profile)

    context = {
        'logged_user': logged_user,
        'f_profile':f_profile,
        'profile': profile,
        'recommended_jobs': recommended_jobs,
        'matched_jobs': matched_jobs,
        'applied_jobs': applied_jobs,
        'companies': companies,
        'user_skills': user_skills,
        'languages': languages,
    }

    return render(request, 'userpanel/userhome.html', context)


@login_required
def add_profile(request):
    logged_user = request.user
    profile, created = CompleteProfile.objects.get_or_create(user=logged_user)

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = logged_user
            profile.save()

            # Handle skills
            skills_data = request.POST.getlist('skills')
            if skills_data:
                profile.skills.clear()
                for skill_name in skills_data:
                    skill, created = Skill.objects.get_or_create(name=skill_name)
                    profile.skills.add(skill)

            # Handle languages
            LanguageProficiency.objects.filter(profile=profile).delete()  # Clear existing languages

            # Get the count of languages dynamically added
            language_count = len([key for key in request.POST if key.startswith('language_')])

            for i in range(language_count):
                language = request.POST.get(f'language_{i}')
                proficiency = request.POST.get(f'proficiency_{i}')
                read = request.POST.get(f'read_{i}', False)
                write = request.POST.get(f'write_{i}', False)
                speak = request.POST.get(f'speak_{i}', False)

                if language and proficiency:
                    LanguageProficiency.objects.create(
                        profile=profile,
                        language=language,
                        proficiency=proficiency,
                        read=read == 'on',
                        write=write == 'on',
                        speak=speak == 'on'
                    )

            return redirect('view_profile')

    else:
        form = CompleteProfileForm(instance=profile)

    languages = LanguageProficiency.objects.filter(profile=profile)

    context = {
        'form': form,
        'languages': languages,
        'logged_user': logged_user
    }
    return render(request, 'userpanel/add_profile.html', context)





@login_required
def view_profile(request):
    logged_user = request.user
    profile = get_object_or_404(CompleteProfile, user=request.user)
    user_skills = profile.skills.all()  # Get user's skills

    # Fetch the language proficiencies associated with the profile
    language_proficiencies = LanguageProficiency.objects.filter(profile=profile)



    context = {
        'profile': profile,
        'languages': language_proficiencies,
        'logged_user': logged_user,
        'user_skills' : user_skills
    }
    return render(request, 'userpanel/view_profile.html', context)


@login_required
def edit_profile(request):
    logged_user = request.user
    profile = get_object_or_404(CompleteProfile, user=request.user)
    
    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('view_profile')
        else:
            # If form is not valid, display the form errors
            messages.error(request, "Please correct the errors below.")
            print(form.errors)
    else:
        form = CompleteProfileForm(instance=profile)

    context = {
        'form': form,
        'logged_user': logged_user,
        'profile' : profile
    }
    return render(request, 'userpanel/edit_profile.html', context)


@login_required
def add_language_proficiency(request):
    logged_user = request.user
    profile = get_object_or_404(CompleteProfile, user=request.user)
    if request.method == 'POST':
        form = LanguageProficiencyForm(request.POST)
        if form.is_valid():
            language_proficiency = form.save(commit=False)
            language_proficiency.user_profile = profile
            language_proficiency.save()
            return redirect('view_profile')
    else:
        form = LanguageProficiencyForm()

    context = {
        'form': form ,
        'logged_user': logged_user,
        'profile' : profile
    }
    return render(request, 'profile/add_language_proficiency.html', context)



def recommended_jobs(request):
    logged_user = request.user
    profile = get_object_or_404(CompleteProfile, user=request.user)
    user_profile = CompleteProfile.objects.get(user=request.user)
    user_skills = user_profile.skills.all()  # Get user's skills

    # Prepare a Q object for matching any of the user's skills
    query = Q()
    for skill in user_skills:
        query |= Q(key_skills__icontains=skill.name)

    # Fetch jobs matching any of the user's skills
    matched_jobs = Job.objects.filter(query).distinct()

    # Get jobs the user has applied for
    applied_jobs = JobApplication.objects.filter(user=logged_user).values_list('job_id', flat=True)

    context = {
        'recommended_jobs': matched_jobs,
        'logged_user': logged_user,
        'applied_jobs': applied_jobs,
        'profile' :  profile,
    }
    
    return render(request, 'userpanel/recommended_jobs.html', context)




def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    # Check if the user has already applied
    if not JobApplication.objects.filter(user=user, job=job).exists():
        # Create a new job application
        job_application = JobApplication.objects.create(user=user, job=job)
        messages.success(request, 'You have successfully applied for this job.')
        print(f"Application created for user {user.username} for job {job.title}.")

        # Create a notification for the company user
        ApplicationNotification.objects.create(
            job=job,
            company_user=job.company.user,  # Assuming the company user is related to the job
            applicant=user,
            message=f'{user.username} has applied for the {job.title} position.',
            created_at=timezone.now()
        )
        print(f"Notification created for company user {job.company.user.username} regarding {job.title}.")
    else:
        messages.error(request, 'You have already applied for this job.')
        print(f"User {user.username} has already applied for job {job.title}.")

    return redirect('userhome')  # Redirect back to the home page



@login_required
def user_notifications(request):
    profile = get_object_or_404(CompleteProfile, user=request.user)
    # Get notifications where the user is the applicant
    # Exclude any notification where the user is also the company user
    received_notifications = NotificationMessage.objects.filter(
        receiver=request.user
    ).order_by('-created_at')

    return render(request, 'userpanel/user_notifications.html', {
        'notifications': received_notifications,
        'profile': profile
    })



@login_required
def all_jobs(request):
    logged_user = request.user
    profile = get_object_or_404(CompleteProfile, user=logged_user)
    
    # Fetch all available jobs from the database
    job_list = Job.objects.all()
    
    # Get jobs the user has applied for
    applied_jobs = JobApplication.objects.filter(user=logged_user).values_list('job_id', flat=True)

    # Paginate with 10 jobs per page
    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Render the jobs in the user panel template
    return render(request, 'userpanel/all_jobs.html', {
        'jobs': page_obj,  # Correctly use paginated jobs
        'applied_jobs': applied_jobs,
        'profile': profile,
        'page_obj': page_obj,  # For pagination navigation
    })


@login_required
def all_companies(request):
    profile = get_object_or_404(CompleteProfile, user=request.user)
    # Fetch all companies
    company_list = CompanyProfile.objects.all()

    # Paginate with 10 companies per page
    paginator = Paginator(company_list, 10)  
    page_number = request.GET.get('page')
    companies = paginator.get_page(page_number)

    return render(request, 'userpanel/all_companies.html', {
        'companies': companies,
         'profile': profile
    })



@login_required
def jobs_by_company(request, company_id):
    # Get the company by ID
    company = get_object_or_404(CompanyProfile, id=company_id)

    # Get all jobs related to this company
    jobs = Job.objects.filter(company=company)

    # Render the jobs and company details in the template
    return render(request, 'userpanel/jobs_by_company.html', {
        'company': company,
        'jobs': jobs
    })


def job_search(request):
    query = request.GET.get('q', '')  # Get the search query from the GET request
    search_results = Job.objects.all()  # Start with all jobs

    if query:
        # Filter jobs based on title, location, or company name
        search_results = Job.objects.filter(
            Q(title__icontains=query) | 
            Q(location__icontains=query) | 
            Q(company__company_name__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'search_results': search_results,
    }
    return render(request, 'userpanel/job_search.html', context)




# View Job
def job_detail(request, pk):
    profile = get_object_or_404(CompleteProfile, user=request.user)
    job = get_object_or_404(Job, pk=pk)
    return render(request, 'userpanel/job_detail.html', {'job': job,'profile':profile })

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('home')
