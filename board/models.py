from django.db import models


class Com2(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads_com2/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Com2File(models.Model):
    document = models.ForeignKey(
        Com2,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='uploads_com2/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Com1_board(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads_com1/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Com1File(models.Model):
    document = models.ForeignKey(
        Com1_board,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    file = models.FileField(upload_to='uploads_com1/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Com2_movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail_image = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Com1_movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail_image = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title