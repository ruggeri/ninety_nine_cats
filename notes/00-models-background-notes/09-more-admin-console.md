## More Admin Console Notes

You can make your own admin classes. Here's how we add inline (AKA
nested) creation of `Toy` objects from the `Cat` admin page.

```python
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

admin.site.register(models.Cat, CatAdmin)
admin.site.register(models.Toy)
```

Next, let's note that we can change what fields are listed in the list
view:

```python
class ToyAdmin(admin.ModelAdmin):
  # When listing toys, also list the cat they belong to. Could be slow
  # because triggers an N+1 query.
  list_display = ['name', 'cat']
```
