from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200) 
    phone = PhoneNumberField()
    subject = models.CharField(max_length=200)
    message = models.TextField()


    class Meta:
        verbose_name_plural = 'Contact Us'
        verbose_name = 'Contact Us'

    def __str__(self):
        return self.full_name
