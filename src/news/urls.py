from django.urls import path
from news import views

urlpatterns = [   
   path('category/<slug:slug>/', views.category_news, name='category_news'),
   path('tag/<slug:slug>/', views.tag_news, name='tag_news'), 
   path('<slug:slug>',views.news_detail, name='news_detail') ,
]