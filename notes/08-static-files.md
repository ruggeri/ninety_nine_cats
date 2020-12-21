## Static Files

We'll create a directory: `cats/static/cats`. In this, we can put our
static files. As with templates, we need the final `cats` folder because
this helps ensure a unique namespacing for the files (since there can be
many static directories, one per app in your project).

So we create a simple `style.css`. And here's how we use it:

```django
{% load static %}

<head>
  <link rel="stylesheet" type="text/css" href="{% static '/cats/style.css' %}">
</head>
```

**TODO**: The `load` part must load extra Django template functionality.
How does that work? Must read the templates docs.

You can see how the `static` function works, though.
