from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class CustomUser(AbstractUser):
    email_verified = models.BooleanField(default=False) #인증 후 true로 바꾼다.
    email_verification_token = models.UUIDField(default=uuid.uuid4) #고유값을 생성한다.
    token_created_at = models.DateTimeField(default=timezone.now)
