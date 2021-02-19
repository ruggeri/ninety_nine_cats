from django.contrib import admin
from . import models

# Can be used to embed many-to-one models
class ToyInline(admin.StackedInline):
  model = models.Toy
  # How many "empty" Toys to add for quick addition on the Cat admin
  # page.
  extra = 0

  # Show a friendly link to the change page.
  show_change_link = True

@admin.register(models.Cat)
class CatAdmin(admin.ModelAdmin):
  search_fields = ['name']

  inlines = [ToyInline]

@admin.register(models.Toy)
class ToyAdmin(admin.ModelAdmin):
  # Avoids an N+1 caused by `cat_age`.
  def get_queryset(self, request):
    queryset = super().get_queryset(request)
    return queryset.prefetch_related('cat')

  # A silly custom field.
  def cat_age(self, toy):
    return toy.cat.age

  search_fields = ['name']
  list_display = ['id', 'name', 'cat_age']
  ordering = ['id']

  # Different ways to render the ForeignKey.
  autocomplete_fields = ['cat']
  # raw_id_fields = ['cat']
  # radio_fields = {'cat': admin.HORIZONTAL}

# filter_horizontal
