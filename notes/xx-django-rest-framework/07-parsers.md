# Parsers

* DRF looks at `Content-Type` header and chooses the appropriate
  parser.
* Default is to parse JSON and form data.
* On individual views, you can set which parser to use.
* The parsed data will be put in the `request.data`.
* You can use `FileUploadParser` to parse raw data that is uploaded. But
  it matches a content type of `*/*` so it should be the only parser
  specified on such a view.
  * Puts the file in `request.data` under the key `'file'`.
* There are 3rd party libs for YAML, XML, MessagePack.
* I believe that whenever you are working with a DRF `Request` object,
  the `.data` will have been subject to parsing.

# Sources

* https://www.django-rest-framework.org/api-guide/parsers/
