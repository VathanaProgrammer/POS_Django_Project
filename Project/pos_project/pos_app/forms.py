from django import forms
from .models import User

# forms.py
from django import forms

class UserRegistrationForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'image']
        widgets = {
            'password': forms.PasswordInput(),  # Ensures password input is masked
        }

    # Optionally add custom validation
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)