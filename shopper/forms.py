from .models import ProductReview
from django.forms import ModelForm, Textarea, RadioSelect

class ReviewForm(ModelForm):
    class Meta:
        GEEKS_CHOICES =[
            ("1", "1"), 
            ("2", '2'), 
            ("3", '3'), 
            ("4", '4'), 
            ("5", '5'), 
        ]
        model = ProductReview
        fields = ['review', 'rating']

        widgets = {
            'review' : Textarea(attrs={
                'class' : 'form-control border-0',
                'placeholder' : 'Your Review *'
            }),
            'rating' : RadioSelect(attrs={
                "required": True,
                'class' : 'fas fa-star'
            }, choices = GEEKS_CHOICES)
        }