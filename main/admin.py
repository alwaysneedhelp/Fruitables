from django.contrib import admin
from main.models import ContactUs

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject']

admin.site.register(ContactUs, ContactUsAdmin)