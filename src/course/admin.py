from django.contrib import admin
from .models import Program,Course,Major,Degree

# Register your models here.
@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    pass

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    pass

@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'program','degree')