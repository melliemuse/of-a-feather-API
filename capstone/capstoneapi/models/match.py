from django.db import models
from .dater import Dater
from .status import Status

class Match(models.Model):
    dater = models.ForeignKey(Dater, on_delete=models.CASCADE, related_name="matching_dater")
    matched_with = models.ForeignKey(Dater, on_delete=models.CASCADE)
    match_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_match = models.DateTimeField(auto_now=True, auto_now_add=False)
