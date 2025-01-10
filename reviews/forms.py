from .models import Reviews
from django.forms import ModelForm, Textarea, RadioSelect

class ReviewsForm(ModelForm):
    class Meta:
        GEEKS_CHOICES =[
            ("1", "1"), 
            ("2", '2'), 
            ("3", '3'), 
            ("4", '4'), 
            ("5", '5'), 
        ]
        model = Reviews
        fields = ['full_text', 'rating']

        widgets = {
            'full_text' : Textarea(attrs={
                'class' : 'form-control',
                'placeholder' : 'Full Review Text'
            }),
            'rating' : RadioSelect(attrs={
                "required": True,
                'class' : 'fas fa-star'
            }, choices = GEEKS_CHOICES)
        }