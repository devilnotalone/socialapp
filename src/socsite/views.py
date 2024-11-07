from django.shortcuts import render, get_object_or_404
from pages.models import Slide
from mediafile.models import MediaFile

def home_view(request):
  media_file = get_object_or_404(MediaFile, id=2)
  media_file_2 = get_object_or_404(MediaFile, id=3)
  slides = Slide.objects.order_by('-order')[:3]
  return render(request, "site/index.html", {'slides' : slides, 'media_file': media_file, 'media_file_2': media_file_2 })

""" def slide(request):
    slides = Slide.objects.order_by('order')  # ดึงสไลด์สามรายการล่าสุด
    return render(request, 'site/slide.html', {'slides': slides}) """