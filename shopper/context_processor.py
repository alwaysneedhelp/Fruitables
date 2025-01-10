from django.shortcuts import render

from profile_page.models import Profile
from .models import Product, Category, Vendor, CartOrder, CartOrderItems, wishlist, Address, ProductImages, ProductReview
from django.db.models import Min, Max

def default(request):
    categories = Category.objects.all()
    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        user_profile = None

    return {
        'categories' : categories,
        'min_max_price' : min_max_price,
        'user_profile' : user_profile,
    }