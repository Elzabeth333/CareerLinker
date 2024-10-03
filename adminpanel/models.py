from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the user
    company_name = models.CharField(max_length=255)
    registration_id = models.CharField(max_length=50, unique=True)  # Add registration ID
    company_logo = models.ImageField(upload_to='media/')
    website = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    def __str__(self):
        return self.company_name




class Job(models.Model):
    class ExperienceChoices(models.TextChoices):
        FRESHER = 'freshers', 'Freshers'
        YEARS_0_2 = '0 - 2 years', '0 - 2 years'
        YEARS_2_4 = '2 - 4 years', '2 - 4 years'
        YEARS_4_6 = '4 - 6 years', '4 - 6 years'
        YEARS_6_8 = '6 - 8 years', '6 - 8 years'
        YEARS_8_PLUS = '8+ years', '8+ years'

    class IndustryChoices(models.TextChoices):
        IT = 'IT Services & Consulting', 'IT Services & Consulting'
        HEALTHCARE = 'Healthcare', 'Healthcare'
        FINANCE = 'Finance', 'Finance'
        RETAIL = 'Retail', 'Retail'
        MANUFACTURING = 'Manufacturing', 'Manufacturing'
        TELECOM = 'Telecommunications', 'Telecommunications'

    class EmploymentTypeChoices(models.TextChoices):
        FULL_TIME = 'FT', 'Full-Time'
        PART_TIME = 'PT', 'Part-Time'
        CONTRACT = 'CT', 'Contract'
        FREELANCE = 'FR', 'Freelance'
        INTERNSHIP = 'IN', 'Internship'

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)  # Link to CompanyProfile
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    openings = models.PositiveIntegerField(default=1)
    selected_candidates = models.IntegerField(default=0)  # Add this field
    role = models.CharField(max_length=100, default='Not specified') 
    employment_type = models.CharField(max_length=50, choices=EmploymentTypeChoices.choices, default=EmploymentTypeChoices.FULL_TIME)
    salary = models.PositiveIntegerField(default=0)  # Using PositiveIntegerField for simplicity
    experience_required = models.CharField(max_length=50, choices=ExperienceChoices.choices, default=ExperienceChoices.YEARS_0_2)
    industry_type = models.CharField(max_length=255, choices=IndustryChoices.choices, default=IndustryChoices.IT)
    key_skills = models.TextField(default="Not specified")
    posted_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company.company_name}"




class CompleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    skills = models.ManyToManyField('Skill', related_name='users',blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    latest_course = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    years_of_experience = models.IntegerField(null=True, blank=True)  # Allow null or provide a default
    current_employer = models.BooleanField(default=False)
    availability_to_join = models.CharField(max_length=50, choices=(
        ('immediately', 'Immediately'),
        ('one_month', 'One Month'),
        ('three_months', 'Three Months'),
        ('more_than_a_year', 'More than a Year')
    ))
    date_of_birth = models.DateField(null=True, blank=True)  # Allowing null values
    gender = models.CharField(max_length=50, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
        ('transgender', 'Transgender')
    ))
    marital_status = models.CharField(max_length=50, choices=(
        ('unmarried', 'Unmarried'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
        ('separated', 'Separated'),
        ('others', 'Others')
    ))
    differently_abled = models.BooleanField(default=False)
    career_break = models.BooleanField(default=False)
    hometown = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    # Language Proficiency will be handled in a separate model


class Skill(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class LanguageProficiency(models.Model):
    profile = models.ForeignKey(CompleteProfile, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=50)
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    speak = models.BooleanField(default=False)

    


class ApplicationNotification(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    company_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')  # Ensure a user can apply to a job only once


#   class Applicant(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
#     resume = models.FileField(upload_to='resumes/')
#     cover_letter = models.TextField(blank=True, null=True)
#     applied_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} applied for {self.job.title}"

# class Bookmark(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='bookmarks')
#     bookmarked_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} bookmarked {self.job.title}"


