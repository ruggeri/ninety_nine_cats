from django.contrib import admin
from . import models

# Can be used to embed many-to-one models
class ToyInline(admin.StackedInline):
  model = models.Toy
  # How many "empty" Toys to add for quick addition on the Cat admin
  # page.
  extra = 0

class CatAdmin(admin.ModelAdmin):
  # Allow them to create toys directly from a Cat object.
  inlines = [ToyInline]

class ToyAdmin(admin.ModelAdmin):
  # When listing toys, also list the cat they belong to. Could be slow
  # because triggers an N+1 query.
  list_display = ['name', 'cat']

admin.site.register(models.Cat, CatAdmin)
admin.site.register(models.Toy, ToyAdmin)
