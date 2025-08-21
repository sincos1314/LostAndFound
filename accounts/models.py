from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = (
    ('M', '男'),
    ('F', '女'),
    ('O', '其他'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    student_id = models.CharField('学号', max_length=32, unique=True)
    college = models.CharField('学院', max_length=64)
    class_name = models.CharField('班级', max_length=64)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES, default='O')
    phone = models.CharField('手机号', max_length=20, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'