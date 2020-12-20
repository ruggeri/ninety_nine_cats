## TODO

* How to setup Postgres?
* Django Rest Framework.
* Various attributes of model properties.
* How associations are done. Go deeper into associated objects/creation.
  * For `ForeignKey`, what are my options? The inverse name appears to be `toy_set`, but I query like `Cat.objects.filter(toy__name="mousey")`?
* Chaining queries onto QuerySet.
* Templates
  * Reduce repetition of loading templates and everything.
* How are form errors handled?

## Tutorials

* Tutorial Pages
  * forms: https://docs.djangoproject.com/en/3.1/intro/tutorial04/
  * testing: https://docs.djangoproject.com/en/3.1/intro/tutorial05/
  * static files: https://docs.djangoproject.com/en/3.1/intro/tutorial06/
  * admin forms: https://docs.djangoproject.com/en/3.1/intro/tutorial07/
* More documentation:
  * https://docs.djangoproject.com/en/3.1/
  * TODO: review to see what additional doc pages are useful.
