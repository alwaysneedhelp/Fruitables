from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.login_home, name='login_home'),
    path('no_account/', views.sign_up, name='sign_up'),
]