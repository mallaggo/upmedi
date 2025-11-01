from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Subject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    # 파일 업로드 방식 (최신/정확)
    video_file = models.FileField(upload_to='videos/')         # 동영상 파일 업로드
    thumbnail_image = models.ImageField(upload_to='thumbnails/')  # 썸네일 이미지 업로드

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
    customuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (by {self.customuser.username})"




# from django.conf import settings
# from django.db import models
#
#
#
# class Category(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
#
# class Subject(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#
#     # URLField 대신 FileField / ImageField
#     video_file = models.FileField(upload_to='videos/')         # 동영상 파일 업로드
#     thumbnail_image = models.ImageField(upload_to='thumbnails/')  # 썸네일 이미지 업로드
#
#     def __str__(self):
#         return self.title
#
# <<<<<<< HEAD
# class Category(models.Model):
#     name = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.name
# class Subject(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     video_url = models.URLField()
#     thumbnail_url = models.URLField()
#
#     def __str__(self):
#         return self.title
#
# def validate_file_size(value):
#     max_size = 5 * 1024 * 1024  # 5MB
#     if value.size > max_size:
#         raise ValidationError(f'파일 크기는 최대 {max_size / (1024*1024)}MB까지 허용됩니다.')
#
# class Post(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField(blank=True)
#     file = models.FileField(upload_to='documents/', validators=[validate_file_size], blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     customuser = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.title} (by {self.customuser.username})"
# =======
# >>>>>>> 99623288505c2081110f25fe78b472112962d213
