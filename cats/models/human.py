from django.contrib.auth import models as auth_models
from django.db import models

# `Human` will replace the standard auth `User` in our application.
class Human(auth_models.AbstractUser):
  related_cats = models.ManyToManyField(
      'Cat',
      through='CatHumanRelationship',
      related_name='related_humans'
  )
