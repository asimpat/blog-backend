from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_details, name='posts'),
    path('post/', views.get_post, name='post'),
    path('register/', views.register, name='register'),

    

]
