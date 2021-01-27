# Model Serializers

* It's common to want a serializer that is closely related to a Django
  model.

```python
# Ports over all fields and their validations. Ports over any model
# level validations.
#
# I'd say this is the one you want to use, right?
#
# ForeignKeys are translated to a `PrimaryKeyRelatedField`. Reverse
# relationships are not included by default. There will be other
# documentation explaining that.
class CatSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cat
    # Strongly encouraged to whitelist so you don't unintentionally
    # expose fields.
    #
    # Fields can be any property or method that takes no argument.
    fields = ['id', 'age', 'view_count']
    # You can specify any fields you don't want them to change. Fields
    # which are editable false (like `id`) are read only by default.
    read_only_fields = ['name']
```

```python
class CatSerializer(serializers.ModelSerializer):
  # Here you say: (1) the serializer field is named `the_name_of_the_cat`,
  # (2) you don't want them to be able to set the field.
  #
  # The point is, you can specify fields explicitly if you want more
  # control.
  the_name_of_the_cat = serializers.CharField(source='name', read_only=True)
  class Meta:
    model = Cat
    fields = ['id', 'age', 'view_count']

class CatSerializer(serializers.ModelSerializer):
  class Meta:
    model = Cat
    fields = ['id', 'name', 'age', 'view_count']
    # Instead of forcing them to entirely override a field, you can
    # specify just some extra kwargs to pass into the serializer field
    # constructor.
    extra_kwargs = { 'name': { 'read_only': True }}
```

## Nested and Related Data

* More information about nesting and relations will be covered later.

## `HyperlinkedModelSerializer`

* Basically, this will use URLs instead of primary key ids.
* When instantiating the serializer, you need to pass the request as
  context. This way, the serializer can know the hostname. Thus,
  fully-qualified URLs can be provided:

```python
serializer = CatSerializer(cat, context={ 'request': request })
# == www.ninety-nine-cats.com/cats/123
serializer.data.url
```

* How are the links generated? The assumption is that we want to send
  people to a url with the name `{model_name}-detail`. It's assumed that
  the pk should be provided as the parameter. This can be customized,
  though.

# Sources

* https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
* https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
