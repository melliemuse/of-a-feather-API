from django.db import models

class Status(models.Model):
    status_type = models.CharField(max_length = 50)