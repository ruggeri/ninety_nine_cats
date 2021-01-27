# Serializer Source Code

## `BaseSerializer`

* Extends `Field`
* Construction:
  * You are not intended to set or modify any fields after construction.
  * You pass an `instance` or initial `data` (or both, or neither).
  * You can tell it whether you want to do a `partial` update. You can
    provide additional `context` to use.
  * If you use `many=True`, there is a `__new__` trick that will
    instantiate a `ListSerializer` that uses this serializer.
* Not implemented:
  * You have to define these yourself:
  * `to_internal_value`: not used in `BaseSerializer`?
  * `to_representation`: used to serialize an instance into a
    representation.
  * `update`, `create`: used when `#save` is called.
* Accessors:
  * `errors`: looks for the `_errors` field set by `is_valid`.
  * `validated_data`: looks for `_validated_data` field set by
    `is_valid`.
* `is_valid`:
  * You call this when you pass initial data.
  * It will call `run_validation`. This is a `Field` method that you
    will probably override in subclasses.
  * Any errors get stored in `_errors`.
  * The validated data gets stored as `_validated_data`. I guess it
    might be cleaned by `run_validation`?
* `save`:
  * Will make sure that you (1) run `is_valid` first, and (2) no errors
    exist.
  * It doesn't want you to call save after touching the data accessor.
    Basically: it doesn't want you to both serialize and deserialize
    using the same `BaseSerializer` instance?
  * If there is an instance, it will cal `update`, else it calls
    `create`.
* `data`:
  * Technically an accessor. Will store serialized value in `_data`
    instance variable.
  * Typically, you'll call `data` only when you have the instance set.
  * This method calls `to_representation`.
  * But if there is no instance, then maybe you can still call
    `to_representation` with the `validated_data`. But won't that just
    be re-serializing what was being validated for
    deserialization/saving? What?

## `SerializerMetaclass`

* `SerializerMetaclass` is used as a trick to find all the Field attributes.

## `Serializer`

* Subclass of both `Serializer` and thus `Field`.
* The point of this is that you will still have to define
  `create`/`update`, but you can leverage `Field` instances and it will
  generate the `to_internal_value` and `to_representation` methods for
  you.
* Fields are tracked by the `SerializerMetaclass`.
* `is_valid`:
  * It will call `to_internal_value`, which itself will validate the
    various fields.
  * After calling `to_internal_value`, we can then call `run_validators`
    to run any validations listed in the `Meta` attribute.
  * TODO: It also calls `validate`, but I don't know what that is
    supposed to do.
* `to_internal_value`:
  * Iterates each writeable field.
  * Gets the field's value from the data (`field.get_value(data)`).
  * Runs the field's validation (`field.run_validation(value)`)
  * Any special validation like `validate_{field_name}` is performed.
  * Will build a dictionary (possibly nested) of the gotten/validated
    values.
* `to_representation`:
  * Iterates through the readable fields.
  * Pulls out the value from the instance:
    `field.get_attribute(instance)`.
  * Stores it in a dictionary.
  * Does no validation of course.

## `ModelSerializer`

* Expects there to be a `Meta` and a `Meta::model`.
* You can specify which fields to serialize using `all`, `exclude`.
  * In the meta, you can specify `extra_kwargs`.
  * You can also always do an explicit definition.
* Properties can be serialized, but only read_only style.
* Nesting:
  * By default, only forward relations are serialized.
  * You can specify the desired depth of nesting.
  * Otherwise, it's going to serialize pks.
  * Nested writes are not allowed by default. You have to define how you
    want this to be done yourself. So you can effectively only do
    nesting with read_only fields.

## TODO

* I have only barely started reading the source code on serializers.

## Sources

* https://github.com/encode/django-rest-framework/blob/master/rest_framework/serializers.py
