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
* Generic views: how are new or create views handled. That wasn't
  explained.
* Must learn about validators!
  * Clean vs validate vs check. They're all Field methods?
  * How to add custom DB constraints?
* How are files/images handled?
* I feel like I'm still a little hazy on 'through' relations.
* And I don't really know how model validation is done.
* And I don't know how to do constraints.

## Tutorials and More Documentation

* All documentation: https://docs.djangoproject.com/en/3.1/

**Model Docs**

* https://docs.djangoproject.com/en/3.1/topics/db
* https://docs.djangoproject.com/en/3.1/ref/models

* https://docs.djangoproject.com/en/3.1/topics/db/examples/
* All other topics have been reviewed and I'm not missing any.

* https://docs.djangoproject.com/en/3.1/ref/models/querysets/#query-related-tools

* https://docs.djangoproject.com/en/3.1/ref/models/lookups/
* https://docs.djangoproject.com/en/3.1/ref/models/relations/
* https://docs.djangoproject.com/en/3.1/ref/models/indexes/
* https://docs.djangoproject.com/en/3.1/ref/models/constraints/
* https://docs.djangoproject.com/en/3.1/ref/models/meta/

* https://docs.djangoproject.com/en/3.1/ref/models/options/
* https://docs.djangoproject.com/en/3.1/ref/models/expressions/
* https://docs.djangoproject.com/en/3.1/ref/models/conditional-expressions/
* https://docs.djangoproject.com/en/3.1/ref/models/database-functions/
* I should review all refs at the end.

* Also, I should make a list of all db topics that I've covered. I
  should rewrite these notes in an order that is sensible and logical to
  me, and that not only covers the information that was given, but that
  also explains to me what I think I should know, but might not have
  been taught.

**Topic Guides**

* All Topic guides: https://docs.djangoproject.com/en/3.1/topics/
* How to install Django https://docs.djangoproject.com/en/3.1/topics/install/
* Migrations https://docs.djangoproject.com/en/3.1/topics/migrations/
* Signals https://docs.djangoproject.com/en/3.1/topics/signals/

* Handling HTTP Requests https://docs.djangoproject.com/en/3.1/topics/http/ (8 pages)
* Working with forms https://docs.djangoproject.com/en/3.1/topics/forms/ (4 pages)
* Templates https://docs.djangoproject.com/en/3.1/topics/templates/
* Class-based views https://docs.djangoproject.com/en/3.1/topics/class-based-views/ (5 pages)
* Managing files https://docs.djangoproject.com/en/3.1/topics/files/
* Testing in Django https://docs.djangoproject.com/en/3.1/topics/testing/ (4 pages)
* User Authentication https://docs.djangoproject.com/en/3.1/topics/auth/ (3 pages)
* Cache Framework https://docs.djangoproject.com/en/3.1/topics/cache/
* Conditional View Processing https://docs.djangoproject.com/en/3.1/topics/conditional-view-processing/
* Cryptographic Signing https://docs.djangoproject.com/en/3.1/topics/signing/
* Sending Email https://docs.djangoproject.com/en/3.1/topics/email/
* Internationalization/Localization https://docs.djangoproject.com/en/3.1/topics/i18n/
* Logging https://docs.djangoproject.com/en/3.1/topics/logging/
* Pagination https://docs.djangoproject.com/en/3.1/topics/pagination/
* Security https://docs.djangoproject.com/en/3.1/topics/security/
* Performance and optimization https://docs.djangoproject.com/en/3.1/topics/performance/
* Serialization https://docs.djangoproject.com/en/3.1/topics/serialization/
* Django Settings https://docs.djangoproject.com/en/3.1/topics/settings/
* System check https://docs.djangoproject.com/en/3.1/topics/checks/
* External packages https://docs.djangoproject.com/en/3.1/topics/external-packages/
* Async support https://docs.djangoproject.com/en/3.1/topics/async/

**How-to Guides**

* All how-to guides: https://docs.djangoproject.com/en/3.1/howto/

**API Reference**

https://docs.djangoproject.com/en/3.1/ref/validators/
https://docs.djangoproject.com/en/3.1/ref/databases/
https://docs.djangoproject.com/en/3.1/ref/schema-editor/
https://docs.djangoproject.com/en/3.1/ref/signals/

https://docs.djangoproject.com/en/3.1/ref/applications/
https://docs.djangoproject.com/en/3.1/ref/checks/
https://docs.djangoproject.com/en/3.1/ref/class-based-views/
https://docs.djangoproject.com/en/3.1/ref/clickjacking/
https://docs.djangoproject.com/en/3.1/ref/contrib/
https://docs.djangoproject.com/en/3.1/ref/csrf/
https://docs.djangoproject.com/en/3.1/ref/django-admin/
https://docs.djangoproject.com/en/3.1/ref/exceptions/
https://docs.djangoproject.com/en/3.1/ref/files/
https://docs.djangoproject.com/en/3.1/ref/forms/
https://docs.djangoproject.com/en/3.1/ref/middleware/
https://docs.djangoproject.com/en/3.1/ref/migration-operations/
https://docs.djangoproject.com/en/3.1/ref/paginator/
https://docs.djangoproject.com/en/3.1/ref/request-response/
https://docs.djangoproject.com/en/3.1/ref/settings/
https://docs.djangoproject.com/en/3.1/ref/templates/
https://docs.djangoproject.com/en/3.1/ref/template-response/
https://docs.djangoproject.com/en/3.1/ref/unicode/
https://docs.djangoproject.com/en/3.1/ref/urlresolvers/
https://docs.djangoproject.com/en/3.1/ref/urls/
https://docs.djangoproject.com/en/3.1/ref/utils/
https://docs.djangoproject.com/en/3.1/ref/views/

## Other

https://github.com/jazzband/django-debug-toolbar/
