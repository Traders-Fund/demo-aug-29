from django import forms
from django.contrib.auth.forms import UserCreationForm
from authuser.models import User
from .models import Program
from django.core.validators import MinValueValidator, MaxValueValidator

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    phone_number = forms.CharField(label="", max_length=15, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    address = forms.CharField(label="", max_length=255, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    city = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    state = forms.CharField(label="", max_length=100, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray- 900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   ', 'placeholder': ''}))
    postcode = forms.CharField(label="", max_length=10, widget=forms.TextInput(
        attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5', 'placeholder': ''}))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'postcode', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].widget.attrs['placeholder'] = ''
        self.fields['first_name'].widget.attrs['placeholder'] = ''
        self.fields['last_name'].widget.attrs['placeholder'] = ''
        self.fields['phone_number'].widget.attrs['placeholder'] = ''
        self.fields['address'].widget.attrs['placeholder'] = ''
        self.fields['city'].widget.attrs['placeholder'] = ''
        self.fields['state'].widget.attrs['placeholder'] = ''
        self.fields['postcode'].widget.attrs['placeholder'] = ''
        
        self.fields['password1'].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   '
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="text-sm text-gray-500 "><li><small>Your password can\'t be too similar to your other personal information.</small></li><li><small>Your password must contain at least 8 characters.</small></li><li><small>Your password can\'t be a commonly used password.</small></li><li><small>Your password can\'t be entirely numeric.</small></li></ul>'
        
        self.fields['password2'].widget.attrs['class'] = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-600 focus:border-violet-600 block w-full p-2.5   '
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="text-sm text-gray-500 "><small>Enter the same password as before, for verification.</small></span>'






class ProgramForm(forms.ModelForm):

    instruments = forms.MultipleChoiceField(
        choices=Program.INSTRUMENT_CHOICES,
      widget=forms.CheckboxSelectMultiple(attrs={'class': 'w-4 text-gray-800  border-gray-300 rounded focus:ring-violet-500'}),  # Add styling here

        required=False
    )

    class Meta:
        model = Program
        fields = [
            'program_name', 
            'program_description', 
            'initial_size', 
            'type_challenge_steps', 
            'trading_period', 
            'maximum_drawdown_limit', 
            'daily_drawdown_limit', 
            'program_first_profit_target', 
            'program_second_profit_target',
            'program_profit_split',  
            'payout_frequency', 
            'instruments', 
            'liquidity_provider'
        ]
        widgets = {
                'program_name': forms.TextInput(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5 '}),
                'program_description': forms.Textarea(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5 '}),
                'initial_size': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5'}),
                'type_challenge_steps': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5  '}),
                'trading_period': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5  '}),
                'maximum_drawdown_limit': forms.NumberInput(attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full ps-10 p-2.5 ',
                    'placeholder': 'Enter a percentage value',
                }),
                'daily_drawdown_limit': forms.NumberInput(attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full ps-10 p-2.5 ',
                    'placeholder': 'Enter a percentage value',
                }),
                'program_first_profit_target': forms.NumberInput(attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full ps-10 p-2.5 ',
                    'placeholder': 'Enter a percentage value',
                }),
                'program_second_profit_target': forms.NumberInput(attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full ps-10 p-2.5 ',
                    'placeholder': 'Enter a percentage value',
                }),
                'program_profit_split': forms.NumberInput(attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full ps-10 p-2.5 ',
                    'placeholder': 'Enter a percentage value',
                }),

                'payout_frequency': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5  '}),

                
                'liquidity_provider': forms.Select(attrs={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-violet-500 focus:border-violet-500 block w-full p-2.5  '})
            }
            
           
        

    # Custom validation for program_name
    def clean_program_name(self):
        program_name = self.cleaned_data.get('program_name')
        if program_name and program_name.isdigit():
            raise forms.ValidationError("Only numbers are not allowed.")
        return program_name

    # Custom validation for program_description
    def clean_program_description(self):
        program_description = self.cleaned_data.get('program_description')
        if program_description and len(program_description) < 50:
            raise forms.ValidationError("The description must be at least 50 characters long.")
        return program_description

     # Custom validation for drawdown limits
    def clean_maximum_drawdown_limit(self):
        maximum_drawdown_limit = self.cleaned_data.get('maximum_drawdown_limit')
        if maximum_drawdown_limit and maximum_drawdown_limit > 100:
            raise forms.ValidationError("It must be a percentage (≤ 100).")
        return maximum_drawdown_limit

    def clean_daily_drawdown_limit(self):
        daily_drawdown_limit = self.cleaned_data.get('daily_drawdown_limit')
        if daily_drawdown_limit and daily_drawdown_limit > 100:
            raise forms.ValidationError("It must be a percentage (≤ 100).")
        return daily_drawdown_limit
    
    def clean_program_first_profit_target(self):
        program_first_profit_target = self.cleaned_data.get('program_first_profit_target')
        if program_first_profit_target and program_first_profit_target > 100:
            raise forms.ValidationError("It must be a percentage (≤ 100).")
        return program_first_profit_target
    
    def clean_program_second_profit_target(self):
        program_second_profit_target = self.cleaned_data.get('program_second_profit_target')
        if program_second_profit_target and program_second_profit_target > 100:
            raise forms.ValidationError("It must be a percentage (≤ 100).")
        return program_second_profit_target
    
    def clean_program_profit_split(self):
        program_profit_split = self.cleaned_data.get('program_profit_split')
        if program_profit_split and program_profit_split > 100:
            raise forms.ValidationError("It must be a percentage (≤ 100).")
        return program_profit_split
    
    def clean_instruments(self):
        # Clean and convert the instruments to a comma-separated string.
        instruments = self.cleaned_data.get('instruments', [])
        return ",".join(instruments)