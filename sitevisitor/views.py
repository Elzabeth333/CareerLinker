from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import  ApplicantRegistrationForm , UserLoginForm , CompanyRegisterForm, CompanyLoginForm , AdminLoginForm
from django.contrib import messages


# Create your views here.



def user_register(request):
    if request.method == 'POST':
        form = ApplicantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful.')
            return redirect('user_login')  # Ensure 'user_login' is the correct name in your URLconf
        else:
            messages.error(request, 'There was an error with your registration. Please try again.')
    else:
        form = ApplicantRegistrationForm()

    return render(request, 'sitevisitor/user_registration.html', {'form': form})



def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Check if user is superuser or staff
                if user.is_superuser or user.is_staff:
                    messages.error(request, "Admins or staff members cannot log in here.")
                else:
                    login(request, user)
                    messages.success(request, "Successfully logged in!")
                    return redirect('userhome')  # Replace with the URL for regular user home
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Form submission is invalid.")
    else:
        form = UserLoginForm()

    return render(request, 'sitevisitor/user_login.html', {'form': form})




def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_superuser:  # Check if the user is a superuser
                    login(request, user)
                    messages.success(request, "Successfully logged in!")
                    return redirect('admin_home')  # Redirect to admin dashboard
                else:
                    messages.error(request, "You don't have permission to access the admin panel.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Form data is invalid.")
    else:
        form = AdminLoginForm()

    return render(request, 'sitevisitor/admin_login.html', {'form': form})




def company_register(request):
    if request.method == 'POST':
        form = CompanyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('company_login')
    else:
        form = CompanyRegisterForm()
    return render(request, 'sitevisitor/company_register.html', {'form': form})




def company_login(request):
    if request.method == 'POST':
        form = CompanyLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('company_home')
                else:
                    messages.error(request, 'You do not have permission to access this page.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CompanyLoginForm()
    return render(request, 'sitevisitor/company_login.html', {'form': form})





def home(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('userhome')  # Redirect to a success page
            else:
                form.add_error(None, 'Invalid username or password')  # Add a non-field error
    else:
        form = UserLoginForm()  # Create an empty form for GET requests
    return render(request, 'sitevisitor/home.html',  {'form': form})




def forgot_password(request):
    return render(request, 'sitevisitor/forgot_password.html')
