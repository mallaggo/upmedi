from django.conf import settings
from django.db import models



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    # URLField 대신 FileField / ImageField
    video_file = models.FileField(upload_to='videos/')         # 동영상 파일 업로드
    thumbnail_image = models.ImageField(upload_to='thumbnails/')  # 썸네일 이미지 업로드

    def __str__(self):
        return self.title

