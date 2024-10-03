from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from adminpanel.models import CompanyProfile
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse

# Create your views here.
def admin_home(request):
    return render(request, 'adminpanel/admin_home.html')


def company_detail(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk)
    return render(request, 'adminpanel/company_detail.html', {'company': company})


def company_list(request):
    companies = CompanyProfile.objects.all()
    context = {
        'companies': companies
    }
    return render(request, 'adminpanel/company_list.html', context)





def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('user_login')