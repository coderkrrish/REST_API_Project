from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.CharField(max_length=30)
    marks = models.IntegerField()
    is_active = models.BooleanField(default = True)


    def __str__(self):
        return (self.name)
    
    class Meta:
        db_table = "B8_REST_Student"
        