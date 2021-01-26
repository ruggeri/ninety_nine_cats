## Admin Console Basics

Start by creating a super user:

```
./manage.py createsuperuser
```

You can now login via `http://localhost:8000/admin/`.

To administer your models, go to `cats/admin.py`:

```python
# cats/admin.py
from django.contrib import admin
from . import models

admin.site.register(models.Cat)
admin.site.register(models.Toy)
```

For free, this will give you admin pages to CRUD your model objects.
