## Permissions

* `has_view_permission`, `has_add_permission`,
  `has_change_permission`, `has_delete_permission`.
* These are used to control access to different admin pages.
* We saw that there are corresponding methods for `InlineAdmin`.

## `get_` methods

* `get_search_results` is a method you can override to change the
  behavior of `search_fields`. This could be pretty useful if you wanted
  to write your own searching logic.
* There are lots of `get_` methods you can use to dynamically calculate
  properties for `ModelAdmin`.
  * Most every property you could set has a `get_` version. This
    includes `get_fields`, `get_exclude`, `get_readonly_fields`,
    `get_list_display`...
  * `get_inlines` is also really helpful. It's newer to Django.
    * Anastassia and I used this to only show inlines if there weren't
      "too many" of them.
    * You could always override `get_inline_instances`, which actually
      instantiates inline classes. But it's a little clunky.

## Admin Routes

If you need to build some URLs, you can use:

1. `admin:{{ app_label }}_{{ model_name }}_changelist`
2. `admin:{{ app_label }}_{{ model_name }}_add` (param: `object_id`)
2. `admin:{{ app_label }}_{{ model_name }}_change` (param: `object_id`)
2. `admin:{{ app_label }}_{{ model_name }}_delete` (param: `object_id`)
