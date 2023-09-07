from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True, help_text='Required. Your full name.')
    email = forms.CharField(max_length=200, required=True)

    class Meta:
        model = Customer
        # fields = UserCreationForm.Meta.fields + ('name', 'email')
        fields = ('name', 'email', 'password1', 'password2')