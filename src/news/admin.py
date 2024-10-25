from django.contrib import admin
from .models import News, NewsCategory, NewsTag, NewsFile

# Register your models here.
class NewsFileInline(admin.TabularInline):
    model = NewsFile  # ใช้โมเดล NewsFile
    extra = 1  # แสดงฟิลด์อัปโหลดไฟล์เพิ่มขึ้นอีก 1 ฟิลด์
    can_delete = True  # เปิดใช้งานการลบไฟล์
    show_change_link = True  # แสดงลิงก์ไปยังหน้าฟอร์มของไฟล์    
    
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('author',)
    inlines = [NewsFileInline] # เพิ่ม Inline สำหรับการอัปโหลดไฟล์    
    
    def delete_model(self, request, obj):
        # ลบไฟล์ที่แนบมากับ News ทั้งหมด เมื่อทำการลบ News
        for file in obj.files.all():
            file.file.delete()  # ลบไฟล์ออกจากระบบไฟล์
        super().delete_model(request, obj)        
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

