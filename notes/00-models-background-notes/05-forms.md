## Forms

We're going to start letting people create new cats. First, we'll add
two new routes:

```python
# cats/urls.py

path('new', views.cats_new, name="new"),
# It's kind of BS, but you can't use URLConf to dispatch based on HTTP
# method. So we have to make a separate create route for now. Later,
# we'll see a class-based approach that will let us dispatch on method.
path('create', views.cats_create, name="create"),
```

Here is our route for `cats_new`:

```python
# cats/views.py

def cats_new(request):
  cat = Cat()
  context = {'cat': cat}
  return render(request, 'cats/cats_new.html', context)
```

And here is our Django HTML:

```django
<!-- cats/templates/cats/new.html -->

<h1>Make a new cat</h1>

<form action="{% url "cats:create" %}" method="POST">
  <!-- The CSRF token input element is embedded here -->
  {% csrf_token %}

  <label>
    Name
    <input type="text" name="name" value="{{ cat.name }}">
  </label>

  <label>
    Age
    <input type="number" name="age" value="{{ cat.age }}">
  </label>

  <input type="submit" value="Create cat!">
</form>
```

## Create Handler

Here is our basic create handler.

```python
# cats/views.py

def cats_create(request: HttpRequest):
  cat = Cat(name=request.POST['name'], age=request.POST['age'])
  cat.save()

  # Trigger a re-direct to the cats:detail page for the newly created
  # cat. Notice how we use `django.urls.reverse` to create a url to
  # redirect to.
  return HttpResponseRedirect(reverse('cats:detail', args=(cat.id, )))
```

Now, if either name or age is not specified by the user, we'll raise a
`KeyError`. But we haven't really worked out yet how to deal with form
errors...
