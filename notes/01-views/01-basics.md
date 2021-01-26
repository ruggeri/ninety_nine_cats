# Class Based Views

## Introduction

To allow reuse via inheritance and mixins, Django has *class-based
views*. If you define `MyCoolView`, you'll write something like this in
the `urls.py`:

```python
urlpatterns = [
  path('cool_view/', MyCoolView.as_view()),
]
```

It is common to subclass views. For instance, we can subclass
`TemplateView`:

```python
# views.py
class MyTemplateView(TemplateView):
  template_name = "my_cool_template.html"

# urls.py
urlpatterns = [
  path('my_route/', MyTemplateView.as_view()),
]
```

The `urlpatterns` don't allow you to specify routing by HTTP method
type. In a function-based view, you can check the the request type:

```python
from django.http import HttpResponse

## Function-based view
def my_view(request):
    if request.method == 'GET':
        # <view logic>
        return HttpResponse('my result content')

## Class-based view
from django import views
from . import models
class CatsIndexView(views.View):
  def get(self, request):
    cats = models.Cat.objects.all()
    cats_str = str(list(cats))
    return HttpResponse(cats_str, content_type="text/text")
```

By default, class-attributes will be available as instance attributes to
the methods. This makes it easy, also, for a subclass to modify behavior
by hiding with a different class variable value. Also, attributes can be
overridden when calling `as_view(attribute_name=replacement_value)`.

They note that they use `Mixins` a fair bit. They note that the upside
is reusability, while the downside is that code gets "scattered to the
four winds."

## Decorators

*This part isn't too important.*

They discuss a bit *decorators*. You can easily apply decorators to
function-based views (FBV). But to apply a decorator to a class-based
view (CBV), you want to decorate the *dispatch* method. The dispatch
method is the one that looks at the request type and decides what kind
of request method to call.

It looks like most decorators from `django` will be written as *function
decorators*. Thus, you need to translate them to a *method decorator*.
You can do this like so:

```python
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProtectedView(TemplateView):
    template_name = 'secret.html'

    # will apply login_required decorator. But you don't normally want
    # to define `dispatch`...
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# So this way is easier. The `name` is specifying the method to
# decorate.
@method_decorator(login_required, name='dispatch')
class ProtectedView(TemplateView):
    template_name = 'secret.html'
```
