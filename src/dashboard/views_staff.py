from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from authuser.models import User
from django.db.models import Count
from .models import TradingAccount , Program
from django.contrib import messages
from .forms import ProgramForm

# Define the check function
def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def dashboard_view_staff(request):
    return render(request, 'pages/staff/dashboard.html')


@login_required
@user_passes_test(is_staff_user)
def traders_view_staff(request):
    # Annotate users with the count of related TradingAccount instances
    normal_users = User.objects.filter(is_staff=False, is_superuser=False).annotate(account_count=Count('trading_accounts'))
    
    context = {
        'normal_users': normal_users,
    }
    return render(request, 'pages/staff/traders.html', context)

@login_required
@user_passes_test(is_staff_user)
def user_trading_accounts(request, user_id):
    selected_user = get_object_or_404(User, id=user_id)
    trading_accounts = selected_user.trading_accounts.all()
    return render(request, 'pages/staff/user_trading_accounts.html', {
        'selected_user': selected_user,
        'trading_accounts': trading_accounts,
    })

@login_required
@user_passes_test(is_staff_user)
def suspend_account(request, account_id):
    account = get_object_or_404(TradingAccount, id=account_id)
    account.account_status = 'suspended'
    account.save()
    messages.success(request, "Account successfully suspended")
    return redirect('user_trading_accounts', user_id=account.user.id)

@login_required
@user_passes_test(is_staff_user)
def programs_view_staff(request):
    programs = Program.objects.all()  # Fetch all programs from the database
    context = {
        'programs': programs,
    }
    return render(request, 'pages/staff/programs.html', context)




# Utility function to check for duplicate programs
def check_duplicate_program(user, type_challenge_steps, exclude_program_id=None):
    queryset = Program.objects.filter(user=user, type_challenge_steps=type_challenge_steps)
    if exclude_program_id:
        queryset = queryset.exclude(id=exclude_program_id)
    return queryset.exists()

@login_required
@user_passes_test(is_staff_user)
def create_program_view(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            program = form.save(commit=False)  # Do not save to the database yet
            program.user = request.user  # Assign the currently logged-in user
            
            # Check for duplicate based on type_challenge_steps
            if check_duplicate_program(request.user, program.type_challenge_steps):
                if program.type_challenge_steps == 'instant':
                    messages.error(request, 'In this demo you are only allowed to have one instant program at a time.')
                elif program.type_challenge_steps == 'challenge':
                    messages.error(request, 'In this demo you are only allowed to have one challenge program at a time.')
            else:
                program.save()  # Save the program to the database
                messages.success(request, "Program successfully created!")
                return redirect('programs_staff')  # Redirect to the program list or another appropriate view
    else:
        form = ProgramForm()

    return render(request, 'pages/staff/create_program.html', {'form': form})


@login_required
@user_passes_test(is_staff_user)
def edit_program_view(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            edited_program = form.save(commit=False)  # Get the unsaved program data
            
            # Check for duplicate based on type_challenge_steps (excluding the current program)
            if check_duplicate_program(request.user, edited_program.type_challenge_steps, exclude_program_id=program.id):
                if edited_program.type_challenge_steps == 'instant':
                    messages.error(request, 'In this demo you are only allowed to have one instant program at a time.')
                elif edited_program.type_challenge_steps == 'challenge':
                    messages.error(request, 'In this demo you are only allowed to have one challenge program at a time.')
            else:
                edited_program.save()  # Save the changes to the database
                messages.success(request, "Program successfully updated!")
                return redirect('programs_staff')  # Redirect to the program list or another appropriate view
    else:
        form = ProgramForm(instance=program)

    return render(request, 'pages/staff/edit_program.html', {'form': form, 'program': program})

@login_required
@user_passes_test(is_staff_user)
def payouts_view(request):
    return render(request, 'pages/staff/payouts.html')


@login_required
@user_passes_test(is_staff_user)
def trading_platforms(request):
    return render(request, 'pages/staff/platforms.html')



@login_required
@user_passes_test(is_staff_user)
def delete_program_view(request, program_id):
    program = get_object_or_404(Program, id=program_id)
    if request.method == 'POST':
        program.delete()
        messages.success(request, "Program successfully deleted!")
    return redirect('programs_staff')


