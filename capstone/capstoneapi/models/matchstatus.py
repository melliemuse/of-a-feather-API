from django.db import models

class MatchStatus(models.Model):
    status_type = models.CharField(max_length = 50)
    