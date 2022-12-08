from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    username.widget.attrs.update({
        'name': 'full_name',
        'id': 'full_name',
        'class': 'input-text'
    })
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password.widget.attrs.update({
        'name': 'password',
        'id': 'password',
        'class': 'input-text'
    })
    
    
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50)
    username.widget.attrs.update({
        'class': 'input-text'
    })
    email = forms.EmailField(required=False)
    email.widget.attrs.update({
        'class': 'input-text'
    })
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password1.widget.attrs.update({
        'class': 'input-text'
    })
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2.widget.attrs.update({
        'class': 'input-text'
    })
    

