from django.contrib import messages
from django.shortcuts import redirect, render

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser != True:
            messages.warning(request, 'You Are Not Authorized to access this page.')
            return redirect('login_home')
        return view_func(request, *args, **kwargs)
    
    return wrapper
        