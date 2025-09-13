from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to="videos/")   # 서버 저장 mp4
    created_at = models.DateTimeField(auto_now_add=True)  # 업로드 날짜

    def __str__(self):
        return self.title


def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(f'파일 크기는 최대 {max_size / (1024*1024)}MB까지 허용됩니다.')

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/', validators=[validate_file_size], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (by {self.customuser.username})"