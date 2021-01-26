# Aggregations

```python
from django.db.models import Avg

# Aggregates an average price over all books.
#
# aggregate is a 'terminal' function. It converts the `QuerySet` into a
# dictionary. Here it is { 'price__avg': ... }.
Book.objects.aggregate(Avg('price'))

# { 'average_price': ... }
Book.objects.aggregate(average_price=Avg('price'))
```

Instead of doing `aggregate`, you can use `annotate`. This is for when
you have a query across one kind of object, but you want to add a field
that describes related objects. For isntance:

```python
from django.db.models import Count
# Will add a books_count field with the number of books for each Author.
Author.objects.annotate(Count('books'))
# You control the name.
Author.objects.annotate(num_books=Count('books'))
```

The docs are clear that trying to do two aggregations won't work,
because a JOIN is used (rather than a subquery):

```python
b = Book.objects.annotate(Count('authors'), Count('store')).get(id=1)
# maybe there are three authors and two stores.
# b.authors__count == 6
# b.authors__count == 6
#
# Because they simply did a JOIN and a COUNT(authors.id), COUNT(store.id).
#
# Note that you can fix this one with a Count('authors', distinct=True).
# But it shows that annotation may not do what you think!
```

Note that you can chain relationships as long as you want.

## Filtering Aggregations

It's easy:

```python
Publisher.objects.filter(authors__name__startswith='M').annotate(m_authors_count=Count('authors'))

# Here's a slightly different way:
Cat.objects.annotate(
  weird_toy_count=Count(
    'toys',
    filter=Q(toys__id__lt=3)
  )
)
# Generates a COUNT(cats_toy.id) FILTER (WHERE cats_toy.id < 3) AS weird_toy_count
# Interesting... I didn't know about this feature.
#
# I believe such a feature will allow you to count toys two different
# ways. E.g., lt 3 and also lt 10. You can have two aggregations.
# So this is really only useful if you're aggregating two different
# ways, I think.
```

They do note some subtleties when you're joining relations multiple
times. For instance:

```python
Publisher.objects.annotate(num_books=Count('book', distinct=True)).filter(book__rating__gt=3.0)
# not the same as
Publisher.objects.filter(book__rating__gt=3.0).annotate(num_books=Count('book'))
# because first query (I think) triggers *two* JOINs.
```

## Other

They note that an annotation field can later be used for an `order_by`.
Here we sort Cats by how many toys they have:

```python
Cat.objects.annotate(Count('toys')).order_by('toys__count')
```

They give one last fancy aggregation:

```python
Book.objects.annotate(num_authors=Count('authors')).aggregate(avg_num_authors=Avg('num_authors'))
```

## List of Aggregations

* Avg
* Count
* Max, Min
* Sum
