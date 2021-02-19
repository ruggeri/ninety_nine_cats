## Django Admin Actions

* You've already seen the bulk deletion action.
* We can write our own actions. They need the form `fn(model_admin,
  request, queryset)`. The `queryset` parameter represents the selected
  items to which the action is being applied.
    * Even better: just write a method on the `ModelAdmin`, and
      reference its by name (string).
* You can set the `short_description` property if you want to.
* You simply set the `actions` property of `ModelAdmin`. Presto!
* If there could be errors, you want to use the `admin.message_user` to
  tell them of the problem.
