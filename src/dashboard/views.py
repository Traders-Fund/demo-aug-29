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



stripe.api_key = settings.STRIPE_SECRET_KEY

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





@login_required
def update_account_name(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        new_account_name = request.POST.get('account_name')

        try:
            account = TradingAccount.objects.get(id=account_id, user=request.user)
            account.account_name = new_account_name
            account.save()
            messages.success(request, 'Account name updated successfully.')
        except TradingAccount.DoesNotExist:
            messages.error(request, 'Account not found or you do not have permission to edit this account.')

    return redirect('account_overview')





def account_overview(request):
    user = request.user
    user_accounts = TradingAccount.objects.filter(user=user)
    
    # Retrieve the selected account name from the GET request
    selected_account_name = request.GET.get('account')
    
    if selected_account_name:
        # Store the selected account name in the session
        request.session['selected_account_name'] = selected_account_name
    else:
        # If no account is selected via GET, try retrieving it from the session
        selected_account_name = request.session.get('selected_account_name')
    
    # Retrieve the selected account object
    if selected_account_name:
        selected_account = user_accounts.filter(account_name=selected_account_name).first()
    else:
        selected_account = None

    current_date = datetime.now().strftime('%Y-%m-%d')

    return render(request, 'pages/account_overview/account_overview.html', {
        'user_accounts': user_accounts,
        'selected_account': selected_account,
        'current_date': current_date,
    })





@login_required
def withdrawal_view(request):
    return render(request, 'pages/withdrawal/withdrawal.html')


@login_required
def profile_view(request):
    if request.method == 'POST':
        if 'public_profile' in request.POST:
         
            request.user.email = request.POST['public_email']
            request.user.save()
            messages.success(request, "Public profile successfully updated!")
        
        elif 'personal_profile' in request.POST:

            request.user.first_name = request.POST['first_name']
            request.user.last_name = request.POST['last_name']
            request.user.phone_number = request.POST['phone_number']
            request.user.address = request.POST['address']
            request.user.city = request.POST['city']
            request.user.postcode = request.POST['postcode']
            request.user.state = request.POST['state']
            request.user.save()
            messages.success(request, "Personal profile successfully updated!")
        
        return redirect('profile') 
    
    return render(request, 'pages/profile/profile.html')




@login_required
def account_list_view(request):
    user = request.user
    trading_accounts = TradingAccount.objects.filter(user=user)
    context = {
        'trading_accounts': trading_accounts,
    }
    return render(request, 'pages/account_list/account_list.html', context)




# Pricing table
pricing_table = {
    'challenge': {
        '2000': 9000,
        '5000': 14500,
        '10000': 35000,
        '25000': 50000,
        '100000': 180000,
        '200000': 290000
    },
    'instant': {
        '2000': 20000,
        '5000': 50000,
        '10000': 90000,
        '25000': 225000,
        '100000': 900000
    }
}


@login_required
def apply_funding(request):
    initial_capital = "Select"
    account_equity = None
    account_type = None
    
    if request.method == 'POST':
        account_equity = request.POST.get('account_equity')
        account_type = request.POST.get('account_type')


        try:
            program = Program.objects.get(type_challenge_steps=account_type)
        except Program.DoesNotExist:
            program = None
        
        if not program:
            messages.error(request, f'No program found matching account type {account_type}')
            return render(request, 'pages/apply_funding/apply_funding.html', {
                'initial_capital': initial_capital,
            })

     
        request.session['account_equity'] = account_equity
        request.session['account_type'] = account_type

        unit_amount = pricing_table[account_type][account_equity]

        product = stripe.Product.create(name=f"{account_type.capitalize()} Trading - {account_equity}")
        price = stripe.Price.create(
            unit_amount=unit_amount,
            currency='usd',
            product=product.id,
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price.id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
    
    if account_equity:
        initial_capital = f"${account_equity}"

    context = {
        'initial_capital': initial_capital,
    }

    return render(request, 'pages/apply_funding/apply_funding.html', context)


@login_required
def update_program(request):
    account_type = request.GET.get('account_type')
    if account_type == 'instant':
        program_instance = Program.objects.filter(type_challenge_steps='instant').first()
    else:
        program_instance = Program.objects.filter(type_challenge_steps='challenge').first()

    if program_instance:
        response = {
            'type_challenge_steps': program_instance.type_challenge_steps,
            'maximum_drawdown_limit': str(program_instance.maximum_drawdown_limit),  # Convert to string to avoid serialization issues
            'daily_drawdown_limit': str(program_instance.daily_drawdown_limit),
            'payout_frequency': program_instance.payout_frequency,
            'program_profit_split': program_instance.program_profit_split,
           
 
        }
    else:
        response = {'error': 'No matching program found'}

    return JsonResponse(response)


def get_next_account_status(user):
    status_sequence = ['active', 'pending', 'challenge', 'suspended']
    # Count the user's existing TradingAccounts
    user_accounts = TradingAccount.objects.filter(user=user).count()
    # Calculate the next status index in the cycle
    next_status_index = user_accounts % len(status_sequence)
    return status_sequence[next_status_index]


@login_required
def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    checkout_session_id = request.GET.get('session_id', None)
    
    if not checkout_session_id:
        return render(request, 'pages/apply_funding/payment_failed.html', {'error': 'No session ID found'})

    try:
        session = stripe.checkout.Session.retrieve(checkout_session_id)
        customer = stripe.Customer.retrieve(session.customer)
    except stripe.error.StripeError as e:
        return render(request, 'pages/apply_funding/payment_failed.html', {'error': str(e)})
    
    user = request.user
    user_payment = UserPayment.objects.get(user=user.id)
    user_payment.stripe_checkout_id = checkout_session_id
    user_payment.save()
    
    if not user.has_bought_first_account:
        user.has_bought_first_account = True
        user.save()

    account_equity = request.session.get('account_equity')
    account_type = request.session.get('account_type')
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))  
    
    if account_equity and account_type:
        try:
            program = Program.objects.get(type_challenge_steps=account_type)
        except Program.DoesNotExist:
            program = None
        
        if program:
            # Get the next account status for the user
            next_status = get_next_account_status(user)

            # Create the new TradingAccount with the calculated status
            TradingAccount.objects.create(
                user=user,
                account_type=account_type,
                account_equity=account_equity,
                account_name=random_string,
                account_status=next_status,  # Set the next status here
                account_maximum_drawdown_limit=program.maximum_drawdown_limit,
                account_daily_drawdown_limit=program.daily_drawdown_limit,
                program_name_of_account=program.program_name,
                first_profit_target=program.program_first_profit_target,
                second_profit_target=program.program_second_profit_target,
                profit_split=program.program_profit_split
            )
        else:
            messages.error(request, f'No program found matching account type {account_type}')
            return render(request, 'pages/apply_funding/payment_failed.html', {'error': f'No program found matching account type {account_type}'})
    
    # Clear session variables
    request.session.pop('account_equity', None)
    request.session.pop('account_type', None)
    
    return render(request, 'pages/apply_funding/payment_successful.html', {'customer': customer})



def payment_cancelled(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	return render(request, 'pages/apply_funding/payment_cancelled.html')




@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = settings.STRIPE_SECRET_KEY
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)