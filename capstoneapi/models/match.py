from django.db import models
from .dater import Dater
from .matchstatus import MatchStatus

class Match(models.Model):
    dater = models.ForeignKey(Dater, on_delete=models.CASCADE, related_name="matching_daters")
    matched_with = models.ForeignKey(Dater, on_delete=models.CASCADE, related_name="matched_with_daters")
    match_status = models.ForeignKey(MatchStatus, on_delete=models.CASCADE, related_name="match_status_daters")
    date_matched = models.DateTimeField(auto_now=False, auto_now_add=True)
