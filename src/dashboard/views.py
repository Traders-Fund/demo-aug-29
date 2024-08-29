from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from dashboard.forms import SignUpForm
from .models import Program, TradingAccount, UserPayment
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import random
import string
import stripe
import time
from django.conf import settings

from django.http import HttpResponse


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

       
       
        user = authenticate(request, username=email, password=password)

        if user is not None:
            print("User authenticated successfully")
            login(request, user)
            messages.success(request, "You've been logged in!")

            
            if user.is_staff:
                return redirect('dashboard_staff')  
            else:
                return redirect('account_overview')  
        else:
            print("Authentication failed")
            messages.error(request, "There was an error logging in, please try again...")
            return redirect('login') 
    else:
        return render(request, 'login/login.html')  
    

def logout_user(request):
	logout(request)
	
	return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Set the password properly using the set_password method
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            # Authenticate using email and password
            email = form.cleaned_data.get('email')
            user = authenticate(email=email, password=password)  # Make sure your backend handles email authentication
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully registered! Welcome!")
                return redirect('account_overview')
            else:
                messages.error(request, "Authentication failed. Please try again.")
        else:
            messages.error(request, "Form is invalid. Please correct the errors.")
    else:
        form = SignUpForm()
    
    return render(request, 'register/register.html', {'form': form})