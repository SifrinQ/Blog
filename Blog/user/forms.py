from django import forms
from django.contrib.auth.models import User
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('hedline', 'rubrick', 'text')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    confirm_password = forms.CharField(max_length = 254, widget = forms.PasswordInput())
    new_password = forms.CharField(required=False, max_length = 254, widget = forms.PasswordInput())


