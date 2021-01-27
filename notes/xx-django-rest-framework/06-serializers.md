# Serializers

## Introduction

* Serializers will convert model objects to pure Python structures that
  can then be rendered XML, JSON style.
* They also will *deserialize*: convert from pure Python structures back
  to model objects.
* They will do validation for you.
* Serializers will buy a house and raise your children for you.
* WHAT CAN'T THEY DO??
* It is stated that serializers work similarly to Django's `Form` and
  `ModelForm` classes. Too bad I don't know how those work!

## Basic Serialization/Deserialization

Here's a `CommentSerializer`:

```python
from rest_framework import serializers

# Define the serializer
class CommentSerializer(serializers.Serializer):
  email = serializers.EmailField()
  content = serializers.CharField(max_length=200)
  created_at = serializers.DateTimeField()

# Do the serialization
serializer = CommentSerializer(comment_object)
# Pythonified data.
serializer.data

from rest_framework import renderers
# Now render the serialized data as JSON.
json = renderers.JSONRenderer().render(serializer.data)
```

An here's it in reverse:

```python
import rest_framework import parsers
jsonData = parsers.JSONParser(jsonStr)
serializer = CommentSerializer(data=jsonData)
# Perform validation
serializer.is_valid()
```

## Creating/Updating Instances

Now, let's talk about how to create/update model instances. You want to
define methods of the serializer:

```python
class CommentSerializer(serializers.Serializer):
  # Data will be validated before passed to create
  def create(self, validated_data):
    comment = Comment(**validated_data)
    comment.save()
    return comment

  def update(self, instance, validated_data):
    for key, value in validated_data:
      setattr(instance, key value)
    instance.save()
    return instance

# Save a new instance
serializer = CommentSerializer(data = jsonData)
comment = serializer.save()

# Update an existing instance
serializer = CommentSerializer(instance, data = jsonData)
comment = serializer.save()
```

## Validation

* `is_valid` will return an object of `{ fieldName: [errors] }`. I think
  `is_valid` will be called always before `save`.
  * Non-field errors will be reported with the key `non_field_errors`.
* You can ask the serializer to do custom validation writing a
  `.validate_{field_name}(value)` method.
  * This method should return the validated value, or raise an instance
    of `serializers.ValidationError`.
* Any further validation can be performed in a `validate(data)` method.
* A third way (easiest way) is to specify `validators=[...]` in the
  field declaration. As in:

```python
def is_named_gizmo(value):
  if value != "Gizmo"
    raise serializers.ValidationError("must be named Gizmo")
  return value

class CatSerializer(serializers.Serializer):
  name = serializers.CharField(validators=[is_named_gizmo])
```

* Last, you can specify validations in the `class Meta` of the
  `Serializer`. This lets you use reusable validations that might
  reference multiple fields.

## Partial Updates

* When instantiating the serializer, you may give the initial
  `instance`. This is the first (optional) positional argument.
* You can also give `initial_data`.

```python
# comment is the existing Comment. `data` is what you want to
# update with.
serializer = CommentSerializer(comment, data=data)
# Gives the comment instance.
serializer.instance
# Gives the data provided. If no data is provided, `initial_data` will
# give an error.
serializer.initial_data

# By default, validation will fail if data doesn't contain some required
# fields. But if you way `partial=True`, the Serializer `is_valid` won't
# try to validate those fields. And, I guess, hopefully the `save` won't
# try to update the fields, either?
serializer = CommentSerializer(comment, data=data, partial=True)
```

## Multiple Objects

It's simple to serialize multiple objects:

```python
serializer = CommentSerializer(multiple_comments, many=True)
# Gives an array of serialized data
serializer.data

# There isn't by default a way to *deserialize* multiple objects.
```

## Nesting

* **TODO**:
  * https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects
  * https://www.django-rest-framework.org/api-guide/serializers/#writable-nested-representations

## TODO

* https://www.django-rest-framework.org/api-guide/serializers/#modelserializer
* https://www.django-rest-framework.org/api-guide/serializers/#hyperlinkedmodelserializer
* https://www.django-rest-framework.org/api-guide/serializers/#listserializer
* https://www.django-rest-framework.org/api-guide/serializers/#baseserializer
* https://www.django-rest-framework.org/api-guide/serializers/#advanced-serializer-usage

## Sources

* https://www.django-rest-framework.org/api-guide/serializers/
