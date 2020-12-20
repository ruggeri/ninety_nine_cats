## Initial Views

Let's add some list and details views/routes. Here are the routes:

```python
# cats/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cats_list, name="list"),
    # Notice the URL parameter
    path('<int:cat_id>', views.cats_detail, name="detail"),
]
```

Next, here are the views:

```python
from django.http import HttpResponse
from django.template import loader
from .models import Cat

def cats_list(request):
  # Fetching models
  cats = Cat.objects.all()
  # Loading templates
  template = loader.get_template('cats/cats_list.html')
  # The template context
  context = {'cats': cats}
  # Rendering!
  return HttpResponse(template.render(context, request))

# The URL parameter gets passed in keyword-style.
def cats_detail(request, cat_id: int):
  cat = Cat.objects.get(id=cat_id)
  template = loader.get_template('cats/cats_detail.html')
  context = {'cat': cat}
  return HttpResponse(template.render(context, request))
```

And now, we make our templates! We put them in `cats/templates/cats/`.
Sigh. Why not just `cats/templates`? It looks like
`django.template.loader` will load a template by name in *any* app's
templates directory: it chooses the first that matches. So we need to
make our template name globally unique by naming it
`cats/cats_list.html`.

Here is our `cats/cats_list.html` template:

```html
{% if cats %}
<ul>
  {% for cat in cats %}
  <li>
    <a href="/cats/{{cat.id}}">{{cat.name}}</a>
  </li>
  {% endfor %}
</ul>
{% else %}
<h1>THERE ARE NO CATS</h1>
{% endif %}
```

Notice that the if will display something different if the `cats` list
is empty. Also note how I laboriously construct the url by hand.
