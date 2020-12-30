from django.db import models

class ToysQuerySet(models.QuerySet):
  def get_mousey(self):
    return self.filter(name='mousey')

class Cat(models.Model):
  class Meta:
    indexes = [
        models.Index(fields=['name']),
    ]

    constraints = [
        models.CheckConstraint(
            check=models.Q(age__gt=0), name="cat_age_gt_zero"
        )
    ]

  name = models.CharField(max_length=255)
  age = models.IntegerField()

  def __str__(self):
    return self.name

class Toy(models.Model):
  objects = ToysQuerySet.as_manager()

  cat = models.ForeignKey(
      Cat,
      on_delete=models.CASCADE,
      related_name="toys",
  )
  name = models.CharField(max_length=255)

  def __str__(self):
    return self.name

class Human(models.Model):
  name = models.CharField(max_length=255)
  related_cats = models.ManyToManyField(
      'Cat',
      through='CatHumanRelationship',
      related_name='related_humans'
  )

class CatHumanRelationship(models.Model):
  cat = models.ForeignKey(
      Cat, on_delete=models.CASCADE, related_name="relationships"
  )
  human = models.ForeignKey(
      Human, on_delete=models.CASCADE, related_name="relationships"
  )
  # Number of years of duration of relationship
  duration = models.IntegerField(default=0)
