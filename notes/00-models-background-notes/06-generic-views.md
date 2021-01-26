## Generic Views

We'll use Django's class-based *generic view system*:

```python
# cats/views.py
from django.views import generic

class CatsListView(generic.ListView):
  template_name = 'cats/cats_list.html'
  # specify what the object list should be called.
  context_object_name = 'cats'

  # Override how objects are queried for the list.
  def get_queryset(self):
    return Cat.objects.order_by('name').all()

class CatsDetailView(generic.DetailView):
  # Will auto infer that context_object_name='cat'
  model = Cat
  # URLConf wants to pass in arg as cat_id.
  pk_url_kwarg = 'cat_id'
  template_name = 'cats/cats_detail.html'

# cats/urls.py
path('', views.CatsListView.as_view(), name="list"),
path(
    '<int:cat_id>/', views.CatsDetailView.as_view(), name="detail"
),
```

There were very minor changes to the detail view:

```django
<h1>{{cat.name}}</h1>

{% if cat.toy_set.all %}
<ul>
  {% for toy in cat.toy_set.all %}
  <li>{{toy.name}}</li>
  {% endfor %}
</ul>
{% else %}
<h3>THERE ARE NO TOYS FOR THIS CAT</h3>
{% endif %}

<a href="{% url "cats:list" %}">Back to cats list</a>
```

It's not clear to me how much of a win this is. I feel like the number
of lines of code did not decrease. Though maybe this is more
'configurationy' than 'codey', which is a plus.
