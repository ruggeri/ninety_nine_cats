# Inlines And `ManyToManyField`

When you have a trivial `ManyToManyField`, Django takes care of you. We
covered this when talking about detail views.

Some trouble comes with a *non-trivial* `ManyToManyField`. This happens
when you explicitly define `through`. Even if the `through` table is a
trivial join table, Django won't help you. You need to do things
explicitly yourself.

This makes sense, because the join table has two `ForeignKeyField`s, and
the objects you care about are both on the reverse side.

You must do it through inlines:

```python
# We'll be able to use this on both sides!
class RelationshipInline(admin.StackedInline):
  model = models.CatHumanRelationship
  extra = 0

class CatAdmin(admin.ModelAdmin):
  fields = ('name', 'age')
  inlines = [RelationshipInline]

  list_display = ('name', 'age')

class HumanAdmin(admin.ModelAdmin):
  fields = ('name', )
  inlines = [RelationshipInline]

  list_display = ('name', )
```

If you throw `search_fields = ['name']` on `CatAdmin, HumanAdmin` and
`autocomplete_fields = ['cat', 'human']` on `RelationshipInline`, you
have a humane way of searching and connecting records.
