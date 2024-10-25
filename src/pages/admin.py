from django.contrib import admin
from .models import Page, PageCategory, PageTag, Slide
from django.utils.html import format_html

@admin.register(PageCategory)
class PageCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(PageTag)
class PageTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published',  'updated_at')
    list_filter = ('category', 'tags', 'is_published', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'image', 'category', 'tags', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    exclude = ('author',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
        
    def is_published_display(self, obj):
        return obj.is_published
    is_published_display.boolean = True
    is_published_display.short_description = 'Published'

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'preview_image')  # ฟิลด์ที่จะแสดงในหน้า list view
    list_editable = ('order', 'is_active')  # ฟิลด์ที่แก้ไขได้โดยตรงในหน้า list view
    search_fields = ('title', 'description')  # เพิ่มช่องค้นหาจาก title และ description
    list_filter = ('is_active',)  # เพิ่มตัวกรองสำหรับสถานะ active
    readonly_fields = ('preview_image',)  # แสดงภาพในหน้า admin
    fields = ('title', 'description', 'image', 'order', 'is_active', 'preview_image')  # ฟิลด์ที่จะแสดงในหน้า form

    # ฟังก์ชันสำหรับแสดงภาพตัวอย่าง
    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "(ไม่มีรูปภาพ)"
    preview_image.short_description = 'Preview'  # เปลี่ยนชื่อหัวข้อคอลัมน์

    