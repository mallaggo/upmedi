from django.db import models

class Com2(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads_com2/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Com2_movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    # URLField 대신 FileField / ImageField
    video_file = models.FileField(upload_to='videos/')         # 동영상 파일 업로드
    thumbnail_image = models.ImageField(upload_to='thumbnails/')  # 썸네일 이미지 업로드
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Com1_movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    # URLField 대신 FileField / ImageField
    video_file = models.FileField(upload_to='videos/')         # 동영상 파일 업로드
    thumbnail_image = models.ImageField(upload_to='thumbnails/')  # 썸네일 이미지 업로드
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Com1_board(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads_com2/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title