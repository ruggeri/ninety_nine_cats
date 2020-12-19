from django.db import models

class Cat(models.Model):
  name = models.CharField(max_length=255)
  age = models.IntegerField()

class Toy(models.Model):
  cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
