from .models import ContactUs
from django.forms import EmailInput, ModelForm, TextInput, Textarea
from phonenumber_field.formfields import PhoneNumberField


class ContactForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'phone', 'subject', 'message']

        widgets = {
            'full_name' : TextInput(attrs={
                'class' : 'w-100 form-control border-0 py-3 mb-4',
                'placeholder' : 'Your Full Name',
                "type" : "text"
            }),
            'email' : EmailInput(attrs={
                'class' : 'w-100 form-control border-0 py-3 mb-4',
                'placeholder' : 'Your Email',
                "type" : "email"
            }),
            'phone' : TextInput(attrs={
                'class' : 'w-100 form-control border-0 py-3 mb-4',
                'placeholder' : 'Your Phone Number (e.g. \'+12125552368\')',
                "type" : "tel"
            }),
            'subject': TextInput(attrs={
                'class': 'w-100 form-control border-0 py-3 mb-4',
                'placeholder': 'Subject',
                'type' : 'text'
            }),
            'message': Textarea(attrs={
                'class' : 'w-100 form-control border-0 mb-4',
                'placeholder': 'Your Message',
                'type' : 'text'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""