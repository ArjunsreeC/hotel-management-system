from django import forms
from .models import User, DIETARY_PREFERENCE_CHOICES, CUSTOMER_TIER_CHOICES
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if len(address) < 5:
            raise ValidationError("Address must be at least 5 characters long.")
        return address

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_validator = EmailValidator()
        email_validator(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

class CustomUserLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

class CustomerSignupForm(forms.Form):
    email = forms.EmailField()
    age = forms.IntegerField()
    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(), initial="test")
    name = forms.CharField(max_length=255)
    tier = forms.ChoiceField(
        choices=CUSTOMER_TIER_CHOICES,
        initial='premium'
    )
    dietary_preference = forms.ChoiceField(
        choices=DIETARY_PREFERENCE_CHOICES,
        initial='custom'
    )