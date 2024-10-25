import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete
from django.core.files.storage import default_storage
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.
def get_image_upload_path(instance, filename):
    # สร้างชื่อไฟล์ใหม่ที่ไม่ซ้ำกัน    
    ext = filename.split('.')[-1]  # รับนามสกุลของไฟล์
    new_filename = f"{uuid.uuid4()}.{ext}"  # สร้างชื่อไฟล์ใหม่ด้วย UUID
    return f'news/images/{new_filename}'  # กำหนดโฟลเดอร์ที่จัดเก็บ   

def get_file_upload_path(instance, filename):
    # สร้างชื่อไฟล์ใหม่ที่ไม่ซ้ำกัน
    ext = filename.split('.')[-1]  # รับนามสกุลของไฟล์
    new_filename = f"{uuid.uuid4()}.{ext}"  # สร้างชื่อไฟล์ใหม่ด้วย UUID
    return f'news/files/{new_filename}'  # กำหนดโฟลเดอร์ที่จัดเก็บ    

# create new model
class NewsCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class NewsTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = HTMLField(null=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.SET_NULL, null=True, related_name='news')
    tags = models.ManyToManyField(NewsTag, related_name='news')
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)  

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
            self.image = None        
        super().delete(*args, **kwargs)  
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # ตรวจสอบว่ามีการเปลี่ยนรูปภาพใหม่หรือไม่
        if self.pk:  
            old_news = News.objects.get(pk=self.pk)  
            if old_news.image != self.image:  
                if old_news.image:  
                    default_storage.delete(old_news.image.name)  

        super().save(*args, **kwargs)  
        # ปรับขนาดภาพ
        if self.image:
            img = Image.open(self.image.path)  # เปิดภาพที่บันทึกลงในไฟล์ระบบแล้ว

            # ปรับขนาดภาพตามความกว้างที่ต้องการ (เช่น 800px)
            max_width = 1024
            if img.width > max_width:
                # คำนวณความสูงตามสัดส่วนเดิม
                new_height = int(max_width * img.height / img.width)
                img = img.resize((max_width, new_height), Image.LANCZOS)
                img.save(self.image.path)  # บันทึกภาพที่ถูกปรับขนาดแล้วทับไฟล์เดิม
    
    
    def get_absolute_url(self):        
        return reverse('news_detail', kwargs={'slug': self.slug})
    
class NewsFile(models.Model):  # เปลี่ยนชื่อจาก ArticleFile เป็น NewsFile
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='news/files/')

    def __str__(self):
        return f"File for {self.news.title}"

@receiver(models.signals.post_delete, sender=News)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    
class Meta:
    ordering = ['order']  

# Signal เพื่อลบไฟล์เมื่อมีการลบ NewsFile ออกจากฐานข้อมูล
@receiver(post_delete, sender=NewsFile)
def delete_file_on_newsfile_delete(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

# Signal เพื่อลบไฟล์เก่าเมื่อมีการอัปโหลดไฟล์ใหม่
@receiver(pre_save, sender=NewsFile)
def delete_old_file_on_change(sender, instance, **kwargs):
    if instance.pk:  # ตรวจสอบว่ามี instance อยู่ในฐานข้อมูลแล้วหรือไม่
        try:
            old_file = NewsFile.objects.get(pk=instance.pk).file
        except NewsFile.DoesNotExist:
            return
        new_file = instance.file
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
  

# Create a reverse relation between News and PageCategory, PageTag
news_category = models.ManyToManyField(NewsCategory, related_name='news')
news_tag = models.ManyToManyField(NewsTag, related_name='news')

