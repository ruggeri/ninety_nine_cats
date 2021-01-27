# BaseSerializer

* This is a parent class of `Serializer`. It basically just doesn't use
  any fields.
* `.data`: the outgoing primitive representation
* `.is_valid()`: method to validate
  * I think this actually maybe calls `to_internal_value`?
* `.validated_data`: the data after validation
* `.errors`: errors encountered during validation
* `.save()`: saves data into an instance.
  * Calls `.update()` and `.create()`
* Reading/writing
  * `to_representation`: this manages conversion of the instance into
    the data.
  * `to_internal_value`: this manages conversion of the data from form
    data (where ints could even be strings) to a format just before what
    you want to call `save` on.
  * You need to write these yourself if using `BaseSerializer` because
    there are no fields/models to guide serialization/deserialization.

In summary: I don't think you want to fuck with this stuff. It's
low-level and not really for the end user to deal with.

## Sources

* https://www.django-rest-framework.org/api-guide/serializers/#baseserializer
* https://www.django-rest-framework.org/api-guide/serializers/#advanced-serializer-usage
