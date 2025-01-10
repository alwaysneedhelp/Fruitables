from .models import Login
from django.forms import ModelForm, TextInput, EmailField


class LoginForm(ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password', 'email']

        widgets = {
            'username' : TextInput(attrs={
                'class' : 'field-wrap',
                'placeholder' : 'Username',
                "type" : "text"
            }),
            'password' : TextInput(attrs={
                'class' : 'field-wrap',
                'placeholder' : 'Password',
                "type" : "password"
            }),
            'email' : TextInput(attrs={
                'class' : 'field-wrap',
                'placeholder' : 'Email',
                "type" : "email"
            })
        }