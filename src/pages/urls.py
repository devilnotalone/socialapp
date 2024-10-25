from django.urls import path
from pages import views

urlpatterns = [
   path('<slug:slug>/', views.page_detail, name='page_detail'),
   path('category/<slug:slug>/', views.category_detail, name='category_detail'),
   path('tag/<slug:slug>/', views.tag_detail, name='tag_detail'), 
]
