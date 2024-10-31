from django.shortcuts import render
from pages.models import Slide,Page

def home_view(request):
  slides = Slide.objects.order_by('-order')[:3]
  return render(request, "pages/home.html", {'slides' : slides})

""" def slide(request):
    slides = Slide.objects.order_by('order')  # ดึงสไลด์สามรายการล่าสุด
    return render(request, 'site/slide.html', {'slides': slides}) """