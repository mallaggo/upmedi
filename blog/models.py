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


class MyCategory(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="카테고리명"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "category"
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리 목록"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MyProduct(models.Model):
    category = models.ForeignKey(
        MyCategory,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="카테고리"
    )

    name = models.CharField(max_length=200, verbose_name="상품명")
    price = models.PositiveIntegerField(verbose_name="가격")
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    short_desc = models.CharField(max_length=255, blank=True)
    stock = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "myproduct"
        ordering = ["-id"]

    def __str__(self):
        return self.name
