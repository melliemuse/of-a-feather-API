from django.db import models
from .dater import Dater
from .match import Match

class Message(models.Model):
    message_body = models.TextField()
    time_sent = models.DateTimeField(auto_now=True, auto_now_add=False)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    logged_in_user = models.ForeignKey(Dater, on_delete=models.CASCADE)