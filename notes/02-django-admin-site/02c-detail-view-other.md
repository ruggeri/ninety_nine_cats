These are some other little helpful features.

## Save Actions

* You can set `save_as = True` to give a "Save as New" option. This
  creates a modified clone.
* You can also add `save_on_top = True` to show save buttons at the top
  of your model.

## View On Site

By default, if `get_absolute_url` is defined on the model, then a "View
on site" button will be generated. You can disable this by setting
`view_on_site = False`.

On the other hand, you can specify a callable. This takes in the model
object, and should return a URL.

## Further Form Customization

* By default, the admin will generate a `ModelForm` for you. I don't
  know very much about `ModelForm` presently; I haven't studied it yet!
* TODO: You can specify the `ModelForm` yourself by setting the `form`
  attribute. I will have to look into this.
* TODO: https://docs.djangoproject.com/en/3.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.formfield_overrides
  * This talks more about how to override some details of the default
    `ModelForm` without writing your own `ModelForm`.
