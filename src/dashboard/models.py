from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone

class Program(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='programs', null=True,  blank=True) # linking the user to the TradingAccount model that he will create
    trading_account= models.ManyToManyField('TradingAccount', related_name='programs', blank=True)
    program_name = models.CharField(max_length=255,null=True)
    program_description = models.TextField(max_length=1000, null=True)
    INITIAL_SIZE_CHOICES = [
        (2500, '$2,500'),
        (5000, '$5,000'),
        (10000, '$10,000'),
        (20000, '$20,000'),
        (25000, '$25,000'),
        (50000, '$50,000'),
        (75000, '$75,000'),
        (100000, '$100,000'),
        (150000, '$150,000'),
        (200000, '$200,000'),
    ]
    initial_size = models.BigIntegerField(choices=INITIAL_SIZE_CHOICES, null=True)
    CHALLENGE_STEP_CHOICES = (
    ('instant', 'Instant'),
    ('challenge', 'Challenge'),
)
    type_challenge_steps = models.CharField(max_length=255, choices=CHALLENGE_STEP_CHOICES, null=True)
    program_status = models.CharField(max_length=255,null=True,blank=True, default='Active')
    TRADING_PERIOD_CHOICES = (
    (4, '4 Days'),
    (7, '7 Days'),
    (14, '14 Days'),
)
    trading_period = models.PositiveIntegerField(choices=TRADING_PERIOD_CHOICES, null=True, help_text='Numbers represents days, only numbers are accepted') 
    maximum_drawdown_limit = models.DecimalField(null=True, max_digits=5, decimal_places=2,default=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')
    daily_drawdown_limit = models.DecimalField( max_digits=5, decimal_places=2, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')
    program_first_profit_target = models.DecimalField( max_digits=5, decimal_places=2, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')
    program_second_profit_target = models.DecimalField( max_digits=5, decimal_places=2, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')
    program_profit_split = models.DecimalField( max_digits=5, decimal_places=2, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')

    PAYOUT_FREQUENCY_CHOICES = (
    (4, '4 Days'),
    (7, '7 Days'),
    (14, '14 Days'),
)
    payout_frequency = models.PositiveIntegerField(choices=PAYOUT_FREQUENCY_CHOICES,null=True)
    INSTRUMENT_CHOICES = [
        ('stocks', 'Stocks'),
        ('fx', 'FX'),
        ('options', 'Options'),
        ('futures', 'Futures'),
    ]
    instruments = models.CharField(max_length=255, null=True, blank=True, help_text="Comma-separated instruments")
    
    LIQUIDITY_CHOICES = [
        ('alaric_securities', 'Alaric Securities'),
    ]
    liquidity_provider = models.CharField(max_length=200, choices=LIQUIDITY_CHOICES, null=True)

    def get_instruments_display(self):
        # This will return a readable display of selected instruments.
        if self.instruments:
            return ", ".join([dict(self.INSTRUMENT_CHOICES).get(item, item) for item in self.instruments.split(",")])
        return ""
    
    def __str__(self):
        return f'{self.program_name} - {self.user} ({self.trading_account.count()} Accounts)' #This will display the program name, user associated with it, and the number of TradingAccount objects linked to the program
    




class TradingAccount(models.Model):
  ACCOUNT_STATUS_CHOICES = [
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('challenge', 'Challenge'),
        ('suspended', 'Suspended'),
    ]
   # Link to program and user
 
  user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trading_accounts', null=True,  blank=True)
  program = models.ManyToManyField(Program, related_name='trading_accounts',  blank=True)# null=True because a user might create an account without immediately linking it to a program.
  
  #what populates when buying
  account_type = models.CharField(max_length=20,null=True, blank=True)#when the user buys account, will also populate this field based on what he selects on the form
  account_name = models.CharField(max_length=20,null=True, blank=True) 
  account_equity = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True) #is what the data use utilize to populate the equity field of account when buying an account, will be the starting state
  payment_type = models.CharField(max_length=40,null=True,blank=True)#Consider renaming this to payment_type and using a separate model PaymentType with choices like "Yearly" or "Monthly". This promotes reusability and avoids redundancy.
  evaluation_starts = models.DateTimeField(auto_now_add=True,blank=True) #ask omar if this is the beggining to the account trading?
  owner_account = models.CharField(max_length=255, null=True,blank=True) #it will be the application dashboard email address, not alarics
  
 #what the prop firm will set and update we pass and populate the fields with the Trading Account model
  program_name_of_account = models.CharField(max_length=255,null=True,blank=True) #maybe I will keep it, gotta find a way to link the program model name with this
  profit_split = models.DecimalField(null=True,blank=True, max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')#propfirm 
  account_maximum_drawdown_limit = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')#propfirm
  account_daily_drawdown_limit = models.DecimalField(blank=True,null=True , max_digits=5,decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')#propfirm
  first_profit_target = models.DecimalField(blank=True,max_digits=10, decimal_places=2 ,null=True )#propfirm
  second_profit_target = models.DecimalField(blank=True,max_digits=10, default=None, decimal_places=2,null=True) #propfirm
  profit_target_achieved = models.BooleanField(blank=True,default=False,null=True)
  account_age = models.DateField(blank=True, null=True) #dont maybe we will include this iny the future
  evaluation_ends = models.DateField(blank=True,null=True)# make calculation to end it somehow
  challenge_steps = models.CharField(max_length=255, blank=True, null=True) #not necessary bc we will modify later
  account_status = models.CharField(max_length=10, choices=ACCOUNT_STATUS_CHOICES, default='active') #not necessary bc we will modify later
  passed_evaluation = models.CharField(blank=True,max_length=255, null=True) #required validation, must be dropdown
  suspended = models.BooleanField(blank=True, default=False,null=True)


  #what comes from ALARIC SECURITIES API
  email_alaric = models.EmailField(unique=True,null=True, blank=True)
  user_code = models.CharField(max_length=20, unique=True,null=True, blank=True,) # dont know if this is suposed to be the django default id, maybe yes.
  password_alaric = models.CharField(max_length=255, unique=True,null=True,blank=True,)
  is_account_used = models.BooleanField(default=False,null=True,blank=True)  # ALARIC API. This account contains the information wether or not the trading account is currently linked to a User. We should write the code in a way that when a User selects a trading programme with the specific parameters, the code searches through the database, identifies an account with the parameters that is unused and links it to the user by putting their username into Column N. If there are multiple available accounts with the exact parameters, the code should select one at random.
  current_drawdown = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], help_text='Enter a percentage between 0 and 100.')#propfirm #from alaric maybe and we do calculations?
  account_pnl = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True) # get from alaric
  time_of_last_profit_received = models.DateTimeField(blank=True, null=True) #get from alaric
  current_profit_number = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  current_profit_percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


  # From Rise API
  total_payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  last_date_of_payout = models.DateField(blank=True, null=True)
  numbers_of_payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  eligible_payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) #make calculations from Rise? #Consider creating a method to calculate eligible_payout
 

  def __str__(self):
    return f"Trading Account ({self.id}) of {self.account_type} program belonging at {self.user.email} " #this must be not a null value
  
  #The __str__ method in a Django model defines the string representation of an instance of the model. This method is called when you convert a model instance to a string, such as when you print it or when it is displayed in the Django admin interface.

#By defining the __str__ method, you control how the model instance will be represented as a string. This is especially useful for making it easier to identify instances of the model when browsing through lists of them, for example, in the Django admin.
  




class UserPayment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    payment_issued_at = models.DateTimeField(default=timezone.now)
    stripe_checkout_id = models.CharField(max_length=500)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_payment(sender, instance, created, **kwargs):
	if created:
		UserPayment.objects.create(user=instance)