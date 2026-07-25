from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class ChatSession(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    last_response_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    last_tool_result = models.JSONField(
        default=dict,
        blank=True
    )

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    role = models.CharField(
        max_length=20
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']



