from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

class AttachmentStyle(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField()
    