from django.db import models
from .dater import Dater
from .matchstatus import MatchStatus

class Match(models.Model):
    dater = models.ForeignKey(Dater, on_delete=models.CASCADE, related_name="matching_dater")
    matched_with = models.ForeignKey(Dater, on_delete=models.CASCADE)
    match_status = models.ForeignKey(MatchStatus, on_delete=models.CASCADE)
    date_matched = models.DateTimeField(auto_now=True, auto_now_add=False)
