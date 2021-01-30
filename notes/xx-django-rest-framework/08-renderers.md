# Renderers

* Content negotiation is performed by DRF. It looks at the `Accept`
  header. Format suffixes can also be used to explicitly ask for a
  particular representation format. You can also specify the renderer
  per view.
* `JSONRenderer`: does what you think.
  * The data in the response will be serialized to JSON.
  * `Response({ key: value })`.
* `TemplateHTMLRenderer`: you return a response with a `template_name`
  specified.
  * The data in the response will be used as the context for rendering
    the template.
  * `Response({ key: value }, template_name="my_template_name.html")`
  * If you specify both `renderer_classes = [TemplateHTMLRenderer,
    JSONRenderer]`, then the same endpoint can serve both kinds of
    content.
* `StaticHTMLRenderer`: you just pass a string as data.
* `BrowsableAPIRenderer`: it renders the data into an HTML presentation
  including clickable links.
* `AdminRenderer`: similar. Renders the data into HTML sort of like the
  Django admin pages.
* `HTMLFormRenderer`: this is part of how forms are going to be
  rendered. TODO: study this more.
* In your code, I think you have to know what kind of renderer might be
  used. Thus, you might want to look at `request.accepted_renderer`.
* I think JSON renderer will try to serialize any exception that is
  thrown.
  * On the other hand, an HTML renderer will search for (1)
    `{status_code}.html` (2) `api_exception.html`, (3) render the status
    code and most basic message.
* There are third party libraries for Yaml, XML,

## Sources

* https://www.django-rest-framework.org/api-guide/renderers
