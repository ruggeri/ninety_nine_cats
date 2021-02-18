# List View Searching

You can list the `search_fields`. This will give you a search text box.
The searching algorithm is simple. Say you search `"John Lennon"`. Then
this is split to the words `"John", "Lennon"`. Next, say you have listed
the fields `search_fields = ['first_name', 'last_name']`. Then the query
performed includes the fragment:

```sql
WHERE (first_name ILIKE '%John%' OR last_name ILIKE '%John%')
  AND (first_name ILIKE '%Lennon%' OR last_name ILIKE '%Lennon%')
```

If you want to be more specific about the field lookup, you can say
`'first_name_exact'`.

By default, only a limited number of results will be shown. Presumably
it is equal to the page size? The total number of matches will be shown
(even though not all the results themselves). Since this is potentially
expensive to compute, you can set `show_full_result_count = False` as an
optimization.
