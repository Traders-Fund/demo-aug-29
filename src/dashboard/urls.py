from django.urls import path
from . import views
from . import views_staff 


urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'), 
    path('apply-for-funding/', views.apply_funding, name='apply_funding'),
    path('account_overview/', views.account_overview, name='account_overview'),
    path('update_account_name/', views.update_account_name, name='update_account_name'),
    path('withdrawal/', views.withdrawal_view, name='withdrawal'),
    path('profile/', views.profile_view, name='profile'),
    path('account-list/', views.account_list_view, name='account_list'),
    

    #STRIPE
    path('payment_successful', views.payment_successful, name='payment_successful'),
	path('payment_cancelled', views.payment_cancelled, name='payment_cancelled'),
    path('update_program/', views.update_program, name='update_program'), 
    path('stripe_webhook', views.stripe_webhook, name='stripe_webhook'),
   

    path('staff/dashboard/', views_staff.dashboard_view_staff, name='dashboard_staff'),
    path('staff/traders/', views_staff.traders_view_staff, name='traders_staff'),
    path('staff/<int:user_id>/accounts/', views_staff.user_trading_accounts, name='user_trading_accounts'),
    path('accounts/suspend/<int:account_id>/', views_staff.suspend_account, name='suspend_account'),
    path('staff/programs/', views_staff.programs_view_staff, name='programs_staff'),
    path('staff/programs/delete/<int:program_id>/', views_staff.delete_program_view, name='delete_program'),
    
    path('create-program/', views_staff.create_program_view, name='create_program'),
    path('staff/programs/edit/<int:program_id>/', views_staff.edit_program_view, name='edit_program'),
    path('staff/payouts/', views_staff.payouts_view, name='payouts'),
    path('staff/platforms/', views_staff.trading_platforms, name='trading_platforms'),

   

   
    ]