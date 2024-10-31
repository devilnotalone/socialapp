import os
import uuid
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.files.storage import default_storage
from tinymce.models import HTMLField
from PIL import Image

def get_image_upload_path(instance, filename):
    # สร้างชื่อไฟล์ใหม่ที่ไม่ซ้ำกัน
    ext = filename.split('.')[-1]  # รับนามสกุลของไฟล์
    new_filename = f"{uuid.uuid4()}.{ext}"  # สร้างชื่อไฟล์ใหม่ด้วย UUID
    return f'pages/images/{new_filename}'  # กำหนดโฟลเดอร์ที่จัดเก็บ   

def get_slide_upload_path(instance, filename):
    # สร้างชื่อไฟล์ใหม่ที่ไม่ซ้ำกัน
    ext = filename.split('.')[-1]  # รับนามสกุลของไฟล์
    new_filename = f"{uuid.uuid4()}.{ext}"  # สร้างชื่อไฟล์ใหม่ด้วย UUID
    return f'pages/slides/{new_filename}'  # กำหนดโฟลเดอร์ที่จัดเก็บ


class PageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PageTag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Page(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = HTMLField(null=True, blank=True)
    category = models.ForeignKey(PageCategory, on_delete=models.SET_NULL, null=True, related_name='pages')
    tags = models.ManyToManyField(PageTag, related_name='pages')
    image = models.ImageField(upload_to=get_image_upload_path, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)  # ฟิลด์สถานะการแสดง 
  
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
        ##จัดการการลบรูปภาพเก่าเมื่อมีการอัปโหลดรูปภาพใหม่
         
        # ตรวจสอบว่ามีการเปลี่ยนรูปภาพใหม่หรือไม่
        if self.pk:  # ถ้าโมเดลมีอยู่แล้ว (ไม่ใช่โมเดลใหม่)
            old_article = Page.objects.get(pk=self.pk)  # ดึงโมเดลเดิม
            if old_article.image != self.image:  # ถ้ารูปภาพเปลี่ยน
                if old_article.image:  # ถ้ามีรูปภาพเดิม
                    default_storage.delete(old_article.image.name)  # ลบรูปภาพเดิม
        super().save(*args, **kwargs)  # บันทึกโมเดล
        
    def get_absolute_url(self):        
        return reverse('page_detail', kwargs={'slug': self.slug})
    
@receiver(models.signals.post_delete, sender=Page)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
# สร้าง slide 
class Slide(models.Model):
    title = models.CharField(max_length=200, null=False)  # ชื่อสไลด์
    description = models.TextField(blank=True, null=True)  # คำอธิบายสไลด์
    image = models.ImageField(upload_to=get_slide_upload_path, blank=True, null=True)
    link = models.URLField(max_length=200, blank=True, null=True)  # ฟิลด์สำหรับลิงก์
    order = models.PositiveIntegerField(default=0)  # ลำดับการแสดงสไลด์
    is_active = models.BooleanField(default=True)  # แสดงผลหรือไม่

    def __str__(self):
        return self.title if self.title else f"Slide {self.pk}"
    
    class Meta:
        ordering = ['order']  # เรียงลำดับตามฟิลด์ order
    
    def save(self, *args, **kwargs):       
         
        # ตรวจสอบว่ามีการเปลี่ยนรูปภาพใหม่หรือไม่
        if self.pk:  # ถ้าโมเดลมีอยู่แล้ว (ไม่ใช่โมเดลใหม่)
            old_article = Slide.objects.get(pk=self.pk)  # ดึงโมเดลเดิม
            if old_article.image != self.image:  # ถ้ารูปภาพเปลี่ยน
                if old_article.image:  # ถ้ามีรูปภาพเดิม
                    default_storage.delete(old_article.image.name)  # ลบรูปภาพเดิม
        super().save(*args, **kwargs)  # บันทึกโมเดล
        
        # ปรับขนาดภาพ
        if self.image:
            img = Image.open(self.image.path)  # เปิดภาพที่บันทึกลงในไฟล์ระบบแล้ว

            # ปรับขนาดภาพตามความกว้างที่ต้องการ (เช่น 800px)
            max_width = 2048
            if img.width > max_width:
                # คำนวณความสูงตามสัดส่วนเดิม
                new_height = int(max_width * img.height / img.width)
                img = img.resize((max_width, new_height), Image.LANCZOS)
                img.save(self.image.path)  # บันทึกภาพที่ถูกปรับขนาดแล้วทับไฟล์เดิม

@receiver(models.signals.post_delete, sender=Slide)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)



