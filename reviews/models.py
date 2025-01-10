from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

    
class Reviews(models.Model):
    full_text = models.TextField('Full Review')
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    rating = models.PositiveIntegerField()


    def __str__(self):
        return f'{self.full_text}'
    
    def get_absolute_url(self):
        return f'/reviews/{self.id}'


    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'