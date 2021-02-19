# Optimizing

*I've probably overthought this.*

Consider the list view for `Toy`s. You can include the owner `Cat`'s
name by writing: `list_display = ['name', 'cat']`. Django admin is smart
and will do an inner join for you.

It does this by using `QuerySet#select_related()`, I think. Basically:
if Django admin sees you use *any* relation like `'cat'`, it will call
`QuerySet#select_related()` *with no arguments*. The behavior of
`select_related` is then to inner join in *all* non-nullable related
objects. Great...

You can override this functionality with
`ModelAdmin#list_select_related`. This is default set to `False`, which
does as described above. If you set it to `True`, it will *always* do
`QuerySet#select_related()` with no arguments. And if you set it to a
list, it will always pass those arguments.

Why would you ever set it explicitly? Firstly, as an optimization to
limit the number of `select_related` tables JOINed. If I only need to
get a `Toy`'s `Cat`, why also fetch any of the toy's other relations?

You might also be using associated data in a way that Django Admin can't
see. For instance, what if you use a `backward_cat` method you define in
the model admin, that uses `toy.cat.name[::-1]`? Django admin can't see
this, and thus won't do the `select_related`.

Last: what if you have something quite a bit more complicated? For
instance, what if we want to show the title of their most recent blog
post?

One way is to override `get_queryset`. Here we can do stuff like
`prefetch_related`, or some kind of weird join, or whatever. This seems
pretty recommended.
