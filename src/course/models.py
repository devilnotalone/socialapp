from django.db import models

# Create your models here.
class Major(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=250)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Degree(models.Model):
    name = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name
    
class Course(models.Model):
    name = models.CharField(max_length=250)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

