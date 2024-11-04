from django.urls import path,include
from accounts import views

urlpatterns = [       
    path('', include('allauth.urls')),
    path('profile/', views.profile, name='profile'),
   
]