from django.db import models
from django.contrib.auth.models import User
from django.db.models import F
from .attachment_style import AttachmentStyle

class Dater(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    attachment_style = models.ForeignKey(AttachmentStyle, on_delete=models.CASCADE, default=None, blank=True, null=True)
    location = models.CharField(max_length=50)
    bio = models.TextField()
    gender = models.CharField(max_length=25)
    gender_preference = models.CharField(max_length=25)
    kids = models.BooleanField()
    smoker = models.BooleanField()
    looking_for = models.CharField(max_length=50)
    interests = models.CharField(max_length=150)
    profile_pic = models.TextField(default=None, blank=True, null=True)
    age = models.IntegerField()
    age_range = models.CharField(max_length=50)
    tagline = models.CharField(max_length=250, default=None, blank=True, null=True)
    been_reported = models.IntegerField(default=None, blank=True, null=True)


    # class Meta:
    #     ordering = (F('user.date_joined').asc(nulls_last=True), )

    # def __str__ (self):
    #     return f'{self.first_name} {self.last_name}'