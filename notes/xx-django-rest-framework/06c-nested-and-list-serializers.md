# Nested and List Serializers

* A serializer class can be used as a a serializer field. Example:

```python
class CatSerializer(serializers.Serializer):
  toys = ToySerializer(many=True)
```

* A big question is how to handle writing nested representations. You
  must write your own `create` and `update` methods in these cases.
* Even `ModelSerializer` won't make nested fields writeable for you.
  It's kind of complicated to know what you will want, so they want you
  to be explicit.
* As mentioned, there will be more documentation later about how
  relations are handled.

* When you specify `many=True`, a `ListSerializer` instance is created.
  But I guess it also will copy the fields off the `CatSerializer`.
* `ListSerializer` will allow for multiple creation, by iterating the
  list and creating each object.
  * You might want to override and use `Cat.objects.bulk_create`.
* They show you one way to do add/remove/update on lists. But it
  involves custom code/is tricky. They don't offer an easy way, because
  it probably isn't a good idea. The semantics are a little weird.

## Sources

* https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects
* https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations
* https://www.django-rest-framework.org/api-guide/serializers/#listserializer
