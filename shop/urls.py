
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('shop/', include('shopper.urls')),
    path('login/', include('login.urls')),
    path('profile/', include('profile_page.urls')),
    path('reviews/', include('reviews.urls')),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
