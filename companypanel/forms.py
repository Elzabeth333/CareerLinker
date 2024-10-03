from django import forms
from adminpanel.models import CompanyProfile , Job


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'registration_id', 'company_logo', 'website', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
        
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'openings', 'role', 'employment_type', 'salary', 'experience_required', 'industry_type', 'key_skills']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'key_skills': forms.Textarea(attrs={'rows': 3}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'openings', 'role', 'employment_type', 
                  'salary', 'experience_required', 'industry_type', 'key_skills', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'key_skills': forms.Textarea(attrs={'rows': 2}),
        }