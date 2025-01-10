from django.db import models


class Login(models.Model):
    username = models.CharField('Username', max_length=50, unique=True)
    password = models.CharField('Password', max_length=50)
    email = models.EmailField('Email', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title
    

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'