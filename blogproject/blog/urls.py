from django.urls import path
from . import views

urlpatterns = [
    path('posts/<int:pk>/', views.post_details, name='post_detail'),
    path('post/', views.get_post, name='post'),
    path('register/', views.register, name='register'),



]
