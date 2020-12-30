# Database Functions

* `Cast(expr, output_field)`: converts an expression to a DB type.
* `Coalesce(*expressions)`: returns first non-NULL value.
* `Greatest`/`Least`: returns greatest/least value.
* `Extract('your_date_field', 'year')`: extracts a part of a date.
  * `Trunc('your_date_field', 'hour'` does similarly, except it keeps
    every up to the hour.
* `Now`: gives the current time on the SQL server.
* Math functions: `Abs`, `Ceil`, `Exp`, `Floor`...
* Bunch of trigonometric functions like `Cos`, `Sin`...
* Strings:
  * `Concat(str1, str2)`
  * `Length(expr)` (returns number of chars in string)
  * `Lower`, `Upper`
  * `Replace(start_str, replacement_target, replacement)`
  * `Reverse` reverses the string
  * `StrIndex(str, search_val)`: finds the position of the search_val in
    the str. 1 indexed!!!
  * `Substr(str, start_pos, len)`: lmao, 1-indexed!

The docs mention that some of these are 'transforms.' For instance, if
you want to search by year, you can say
`Cat.objects.filter(birthday__year=2000)`. `year` is a transform of any
`DateTime`.

Likewise, the various math functions (e.g., `Abs`, `Cos`, etc), as well
as the string functions (e.g., `Length, Lower, Upper`) methods are
transforms.

They discuss some window function crap but I don't care.
