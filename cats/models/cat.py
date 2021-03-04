from django.db import models
from .human import Human

class CatPermissions:
  SAY_HELLO_TO_CAT = "say_hello_to_cat"

class Cat(models.Model):
  Permissions = CatPermissions

  class Meta:
    indexes = [
        models.Index(fields=['name']),
    ]

    constraints = [
        models.CheckConstraint(
            check=models.Q(age__gt=0), name="cat_age_gt_zero"
        )
    ]

    permissions = [
        (CatPermissions.SAY_HELLO_TO_CAT, "Say hello to the cat")
    ]

  # Properties of a Cat.
  name = models.CharField(max_length=255)
  age = models.IntegerField()
  view_count = models.IntegerField(default=0)

  def __str__(self):
    return self.name

  def say_hello(self, human: Human):
    if not human.has_perm(CatPermissions.SAY_HELLO_TO_CAT):
      raise Exception(f"{human} is not allowed to say hello to cats")

    print(f"{human} says hello to {self}")
