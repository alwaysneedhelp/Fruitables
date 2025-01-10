from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from .models import Reviews
from .forms import ReviewsForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.forms import formset_factory

def review_home(request):
    reviews = Reviews.objects.order_by('-date')
    return render(request, 'reviews/reviews_home.html', {'reviews' : reviews, 'numbers' : range(1,6)})


class ReviewDetailView(DetailView):
    model = Reviews
    template_name = 'reviews/details_view.html'
    context_object_name = 'article'

class ReviewUpdateView(UpdateView):
    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author == self.request.user or self.request.user.is_superuser:
            print(obj)
            return obj #or Http404
        raise exceptions.PermissionDenied()
    
    model = Reviews
    form_class = ReviewsForm
    template_name = 'reviews/update.html'
    success_url = "/reviews"

class ReviewDeleteView(DeleteView):
    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if obj.author == self.request.user or self.request.user.is_superuser:
            return obj #or Http404
        raise exceptions.PermissionDenied()
    model = Reviews
    success_url = '/reviews/'
    template_name = 'reviews/reviews_delete.html'


def error(request):
    return render(request, 'reviews/error.html')

@login_required(login_url="/login/")
def create(request):
    error = ''
    if not Reviews.objects.filter(author=request.user).exists() or request.user.is_superuser:
        if request.method == 'POST':
            form = ReviewsForm(request.POST)
            if form.is_valid():
                form.instance.rating = request.POST.get('rating')
                form.instance.author = request.user
                form.save()
                return redirect('review_home')
            else:
                error = 'NOT CORRECT DATA'
    else:
        return redirect('error_review')
    form = ReviewsForm()

    data = {
        'form' : form,
        'error' : error,
    }
    
    return render(request, 'reviews/create.html', data)