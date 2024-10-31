from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class prefix_name(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name 

# นักศึกษา (Student Model)
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=10, unique=True)
    prefix_name = models.ForeignKey(
        prefix_name, on_delete=models.CASCADE, verbose_name="คำนำหน้านาม"
    )
    fname_th = models.CharField(max_length=150, verbose_name="ชื่อ (ภาษาไทย)")
    lname_th = models.CharField(max_length=150, verbose_name="สกุล (ภาษาไทย)")
    department = models.CharField(max_length=255)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.student_id})" 