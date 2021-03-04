from django.db import models

class Toy(models.Model):
  name = models.CharField(max_length=255)

  cat = models.ForeignKey(
      "Cat",
      on_delete=models.CASCADE,
      related_name="toys",
  )

  def __str__(self):
    return self.name
