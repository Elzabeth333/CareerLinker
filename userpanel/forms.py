from django import forms
from adminpanel.models import  LanguageProficiency , Skill , CompleteProfile 

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = CompleteProfile
        fields = [
            'bio', 'profile_image',  'location', 'resume', 'cover_letter', 
            'latest_course', 'university', 'mobile_number', 'years_of_experience', 
            'current_employer', 'availability_to_join', 'date_of_birth', 'gender', 
            'marital_status', 'differently_abled', 'career_break', 'hometown', 'pincode'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            
        }

class LanguageProficiencyForm(forms.ModelForm):
    class Meta:
        model = LanguageProficiency
        fields = ['language',  'read', 'write', 'speak']
        
        widget={
            'proficiency':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Good/Very good/Excellent'})
        }


class CompleteProfileSkillForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Display skills as checkboxes or another widget if needed
        required=False
    )

    class Meta:
        model = CompleteProfile
        fields = ['skills']
