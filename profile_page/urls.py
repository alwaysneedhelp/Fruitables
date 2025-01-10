from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Add this
    path('', profile, name = 'profile'),
    path('logout/', logout_func, name = 'mylogout'),
    path('order/<int:id>/', order_detail, name='order-detail'),
    path('change_password/', change_password, name='change_password')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)