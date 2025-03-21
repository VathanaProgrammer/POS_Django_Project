from django import forms
from .models import User  # Assuming you have a custom User model

# forms.py
from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('Admin', 'Admin'), ('Cashier', 'Cashier')])
    image = forms.ImageField()

    # Optionally add custom validation
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)