from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_reviews, name='get_reviews'),  # GET /reviews/
    path('create/', views.create_review, name='create_review'),  # POST /reviews/create/
]
