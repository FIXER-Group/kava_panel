from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import User

class LoginAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']
    def __init__(self, *args, **kwargs):
        super(LoginAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control fadeIn second', 'placeholder': 'login'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control fadeIn third', 'placeholder':'password'}) 