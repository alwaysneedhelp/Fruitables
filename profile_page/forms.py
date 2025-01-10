
from django.forms import ChoiceField, ModelForm, RadioSelect, TextInput, EmailField
from phonenumber_field.formfields import PhoneNumberField

from profile_page.models import Profile
from shopper.models import Address


class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'mobile', 'status']

        CHOICES_STATUS = [
            (True, 'Active'),
            (False, 'Not Active')
        ]

        widgets = {
            'address' : TextInput(attrs={
                'placeholder' : 'Address',
                "type" : "text"
            }),
            'mobile' : TextInput(attrs={
                'placeholder' : 'Phone Number',
                "type" : "tel"
            }),
            'status' : RadioSelect(
                choices= CHOICES_STATUS,
            )
        }

""" class ProfileForm(ModelForm):
    class Meta:
        model = Profile
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
        } """