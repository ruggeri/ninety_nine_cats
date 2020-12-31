# Itinerary

## Basic Models

**00 Basic Models**

* Create a `Cat` model to demonstrate some simple fields.
* `db_column` will control the name of the db field.
* You can set `Meta::db_table` to change the table name.
* Field types
  * `AutoField`
  * `CharField`
  * `DateField`, `DateTimeField`
  * `TextField`

**01 Migrations/REPL**

* Show how to create migrations. Show how to print their SQL.
* Show basic querying in the REPL. Show shell_plus with --print-sql.

**02 CRUD Actions**

* The `save` method will do an INSERT if there is no primary key
  present. If a primary key is present, an UPDATE will be issued.
* `#delete` can be called on either a single item, or a query set.
* You can call `update` on a `QuerySet`. This lets you do a bulk update
  operation. This is a good use case for `F` expressions.
* `Cat.objects.get_or_create`, `Cat.objects.update_or_create`.
* `Cat.objects.bulk_create(Cat(...), Cat(...))`: efficiently create many
  objects at once.
* `Cat.objects.in_bulk(ids)`: efficiently query a map of many Cat
  objects.
* `#refresh_from_db` will refetch the object.

**03 Basic QuerySet**

* `Cat.objects` is a 'manager.' But it is almost a `QuerySet`.
* Lazy query building. Caching of results.
  * `iterator` method will make a `QuerySet` uncached.
* Can `filter` by field.
* You can call `get` if there is exactly one result.
* If you slice a query set, you will issue a LIMIT and OFFSET.
* `order_by`
  * TODO: what is the deal with order_by with a distinct?
* `values` will pull regular objects rather than model objects.
* You may call `defer` if you want to defer some fields. Then a getter
  will fetch the needed data if ever requested. This is for optimization
  purposes.

**04 QuerySet Matchers**

* `iexact`
* `contains`, `icontains`
* `startswith`/`istartswith`, `endswith`/`iendswith`,
* `in`: you give a list of values
  * Here, you can use a nested query!
* `gt`, `lt`
* `isnull`
* `regex`

## Basic Relations

**05 ForeignKey Relationship**

* Create a `Toy` model to demonstrate a `ForeignKey` relationship.
  * Choose `related_name` to be `toys`. Note it is otherwise called
    `toy_set`.
    * You can also note about `related_query_name`, which will by
      default be `toy` but will be set to whatever you choose as
      `related_name` (if specified).
    * You can specify the foreign key with `to_field`. But this is
      usually unnecessary.
  * Show how this gets loaded. Show the `__dict__` which demonstrates
    the foreign key.
* Set the `on_delete` option to determine CASCADE behavior.
* Initial request will query and then cache.
* Reverse relation `cat.toys` will not cache.

**06 ManyToMany Relationship**

* Create a `Human` model to demonstrate a `ManyToMany` relationship.
* This will create a join table for you. The JOIN table has the three
  indices you expect: `fk1`, `fk2`, `(fk1, fk2)`.
* To ensure symmetry, you may want to set the `related_name` explicitly.
* You can set up your own join table, in case you want to hold
  additional information there. Then you specify the `related_name`
  attribute.
* **TODO**: Can you traverse multiple relations a la ActiveRecord?

**07 OneToOneField**

* Similar to a `ForeignKeyField` with `unique=True`. But more
  convenient, because reverse relationship will be just a getter rather
  than a manager object.
* Most useful for multi-table inheritance.

**08 Relation CRUD Methods**

* Setting `toy.cat = cat` will set `toy.cat_id`.
* You can call `cat.toys.add(toy)` which will set the `toy.cat_id` field
  and save the record.
* `cat.toys.create(...)`
* You can `remove` objects, or `clear` all objects. With the reverse of
  a `ForeignKeyField`, this only works if the field is nullable

**09 Filtering Across Relations**

* If you write `Cat.objects.filter(toys__name='mousey')`, a JOIN is
  issued. A cat is returned if it has an associated toy named mousey.
* But this will cause the same record to be returned multiple. So you
  may want to be careful.
* You may want to use `distinct`.

**10 Prefetching Related Objects**

* `select_related` This is used for `Toy.objects.select_related('cat')`.
* `prefetch_related` will issue a second query to fetch the related
  objects. It will then stitch them together. There's even a nice helper
  function to do this on a list of objects.
* You can create a `Prefetch` object if you want to specify an
  `order_by`, `limit`, `filter`...

## Advanced Querying: Annotation and Aggregation

**Q and F Expressions**

* An `F` expression can be used anywhere a column name is needed. For
  instance, `Cat.objects.filter(toys__name=F('name'))`.
  * TODO: How do you know what table `name` resides in?
* A `Q` expression lets you declare a filtering query. For instance, if
  you wanted to find all rows that matched one of two conditions, you
  could issue: `Cat.objects.filter(Q(name='Markov') | Q(age=10))`.

**Aggregation**

* There are many aggregation functions like `Avg`, `Count`, `Max`,
  `Min`, `Sum`.
* If you aggregate a field, you'll collapse the table. You can name
  aggregations.

**Annotation**

* This allows you to add additional fields. Useful for doing
  aggregations from related tables.
* Be careful though. JOINs are used rather than subqueries. So doing
  multiple counts in one annotation is probably going to go wrong.

## Concurrency, Indexing, Constraints

**Concurrency/Transactions**

* Show an example where `F` is used.
* Mention that `update_fields=[...]` can be used.
* `django.db.transaction.atomic` decorator.
  * Can also use it as a context manager.

**Indexes**

* You add them to `Meta::indexes`. You can specify the set of fields to
  index on.
* For single column index, you can just set `db_index=True` on the
  field.

**Constraints**

* Constraints are not validations. They won't raise validation errors.
  But they will raise DB integrity errors if you try to save.
* `UniqueConstraint` is best specified via `unique=True`.
  * Except sometimes you want a unique constraint across several fields.
* You can also add `models.CheckConstraint`. You specify a `Q`
  expression that must always be true.

## Models And Inheritance

**Abstract Base Classes**

* You can set `Meta::abstract`.
* This is good for extending a default model class with more
  functionality.
* You're more likely to use these kinds of classes from a contrib
  library than write them yourself.

**Multi Table Inheritance**

* Define a `Place` class. Then consider a `Restaurant` *is a* `Place`.
* You can inherit `Restaurant` from `Place`. Django will create the
  `OneToOneField` for you. When you query a `Restaurant`, I think Django
  will query `Place` also and fetch the fields.
* You can also downcast by writing `place.restaurant`. If the specified
  place is not a restaurant, an exception is raised.
* Crazy, but you can even do *multiple* inheritance. Wow that sounds
  like a bad idea.

## Uncategorized?

**Validation**

* blank, null field options.
* unique validation.
* You can add a `validators` property, but we won't discuss.
* We won't talk about signals, but I'll just note that overriding
  save/et cetera is probably not what you want. However, there are many
  circumstances where signals aren't fired anyway.
* `full_clean`: `clean_fields`, `clean`, `validate_unique`
  * Not called on model `#save`! You must call it yourself.

**Other/Esoterica**

* Talk about `QuerySet::as_manager`. Show how you can extend a
  `QuerySet` with new querying methods.
* `QuerySet#raw`. Interpolation.
* You can build a CASE/WHEN with Django. But it's whack.
* There are a bunch of DB functions, but I don't know when I would use
  any of those?
* `FileField`, `ImageField`.

## TODO

* Need to finish review of the expressions ref page.
