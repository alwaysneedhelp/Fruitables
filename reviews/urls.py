from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.review_home, name='review_home'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/update', views.ReviewUpdateView.as_view(), name='review_update'),
    path('<int:pk>/delete', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('error', views.error, name='error_review')
]