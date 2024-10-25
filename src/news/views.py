from django.shortcuts import render, get_object_or_404
from .models import News, NewsCategory ,NewsTag

# Create your views here.

def news_detail(request, slug):
    news = get_object_or_404(News, slug=slug)
    if not news.is_published:
        return render(request, 'news/news_not_published.html', {'news': news})
    return render(request, 'news/news_detail.html', {'news': news})

def category_news(request, slug):
    category = get_object_or_404(NewsCategory, slug=slug)   
    news = category.news.all()
    return render(request, 'news/category_news.html', {'category': category,'news': news})

def tag_news(request, slug):
    tag = get_object_or_404(NewsTag, slug=slug)
    news = tag.news.all()
    return render(request, 'news/tag_news.html', {'tag': tag,'news': news})