# Transactions

In `settings.py`, you can set `ATOMIC_REQUESTS = True` to run every view
function in a transaction.

You can use the `django.db.transaction.atomic` decorator to decorate
functions so that they run in their own transaction. You can also use
this as a "context manager:"

```python
from django.db import transaction

@transaction.atomic
def cool_function():
  pass

def cool_function_two():
  # A context manager is anything with __enter__ and __exit__ methods.
  with transaction.atomic():
    # do some cool stuff
    pass

def cool_function_three():
  model = Model.objects.get(id=123)
  model.xyz = 123
  try:
    with transaction.atomic():
      model.save()
      # do some cool stuff
      pass
  except IntegrityError:
    # catch a DB IntegrityError. An IntegrityError occurs, for instance,
    # when a foreign key check fails. E.g., maybe someone deletes a
    # referenced object out from under you. As in: you didn't do S2PL
    # and thus problems are surfaced at the COMMIT point?
    #
    # Since model.xyz didn't get saved, you might want to reset it.
    pass
```

They warn you from catching DB errors when in a transaction.

You can use `transaction.on_commit` while in a transaction to schedule a
task that should be run when the current transaction commits:

```python
@transaction.atomic
def do_cool_stuff():
  # ...
  transaction.on_commit(lambda: send_confirmation_email())
```

They mention that if you have `on_commit` actions scheduled, you can't
use the basic `TestCase`. You must use `TransactionTestCase`. This is
because `TestCase` uses transactions to rollback database updates in the
test.

They mention various low-level transaction methods. We don't need them.
