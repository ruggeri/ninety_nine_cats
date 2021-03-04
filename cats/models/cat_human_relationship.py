from django.db import models

class CatHumanRelationship(models.Model):
  cat = models.ForeignKey(
      "Cat", on_delete=models.CASCADE, related_name="relationships"
  )

  human = models.ForeignKey(
      "Human", on_delete=models.CASCADE, related_name="relationships"
  )

  # Number of years of duration of relationship
  years_of_durations = models.IntegerField(default=0)
