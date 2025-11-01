from django.db import models

class Com2(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    upload = models.FileField(upload_to='uploads_com2/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
