from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import ContactForm
from shopper.models import Product
from django.contrib import messages

def home(request):
    products = Product.objects.all().order_by('-date')

    context = {
        'products' : products,
    }

    return render(request, 'main/index.html', context)

def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your request to contact has been successfully sent to the server!')
            return HttpResponseRedirect(request.get_full_path())
        else:
            fields = ['full_name', 'email', 'phone', 'subject', 'message']

            translator = {
                'full_name' : 'Full Name',
                'email' : 'Email',
                'phone' : 'Phone Number',
                'subject' : 'Subject',
                'message' : 'Message',
            }

            missing_fields = []

            for a in fields:
                if a in form.cleaned_data.keys():
                    pass
                else:
                    missing_fields.append(translator[a])


            missing_fields = ', '.join(missing_fields)

            messages.error(request, f'Fill in these fields right please: {missing_fields}')
            print(form.cleaned_data)
            print('not valid form')

    form = ContactForm

    context = {
        'form': form
    }

    return render(request, 'main/contact.html', context)


def ajax_contact(request):
    pass