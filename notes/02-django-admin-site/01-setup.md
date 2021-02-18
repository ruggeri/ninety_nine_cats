# Setting Up The Django Admin

You must start by running `./manage.py createsuperuser` to create a user
to administer the admin panel. You must update your project's primary
urls like so:

```python
from django.contrib import admin

urlpatterns = [
    # Project paths...
    path('cats/', include('cats.urls')),

    # Admin paths.
    path('admin/', admin.site.urls),
]
```

Any application can now register admin views:

```python
admin.site.register(models.Cat, CatAdmin)

# Create subclasses of admin.ModelAdmin
class CatAdmin(admin.ModelAdmin):
  pass

class ToyAdmin(admin.ModelAdmin):
  pass

# register these admins for the corresponding models.
admin.site.register(models.Cat, CatAdmin)
admin.site.register(models.Toy, ToyAdmin)

# alternatively:

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
  pass
```

You now have `admin/cats/cat` and `admin/toys/toy` routes. Django Admin
will look for an admin module in each of your applications and import
it. This is how it discovers your admin pages.
