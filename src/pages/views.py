from django.shortcuts import render, get_object_or_404
from .models import Page, PageCategory, PageTag, Slide

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if not page.is_published:
        return render(request, 'pages/page_not_published.html', {'page': page})
    return render(request, 'pages/page_detail.html', {'page': page})

def category_detail(request, slug):
    category = get_object_or_404(PageCategory, slug=slug)
    pages = category.pages.all()    
    return render(request, 'pages/category_detail.html', {'category': category, 'pages': pages})

def tag_detail(request, slug):
    tag = get_object_or_404(PageTag, slug=slug)
    pages = tag.pages.all()
    return render(request, 'pages/tag_detail.html', {'tag': tag, 'pages': pages})

""" def slide(request):
    slides = Slide.objects.order_by('order')  # ดึงสไลด์สามรายการล่าสุด
    return render(request, 'pages/slide.html', {'slides': slides}) """
    