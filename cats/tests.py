from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from .models import Cat

class CatModelTests(TestCase):
  def test_cat_must_have_name(self):
    cat = Cat()
    cat.name = ""
    cat.age = 123

    with self.assertRaises(ValidationError) as context_manager:
      cat.full_clean()

    err: ValidationError = context_manager.exception
    err = err.error_dict['name'][0]
    self.assertEqual(err.message, "This field cannot be blank.")

  def test_cat_must_have_age(self):
    cat = Cat()
    cat.name = "Markov"

    with self.assertRaises(ValidationError) as context_manager:
      cat.full_clean()

    err: ValidationError = context_manager.exception
    err = err.error_dict['age'][0]
    self.assertEqual(err.message, "This field cannot be null.")

class CatsListViewTests(TestCase):
  def test_cats_are_listed(self):
    cat = Cat(name="Markov", age=123)
    cat.save()
    cat = Cat(name="Gizmo", age=123)
    cat.save()

    # Get the webpage.
    response = self.client.get(reverse("cats:list"))

    # Check the response code.
    self.assertEqual(response.status_code, 200)

    # Check that the HTML contains certain text.
    self.assertContains(response, "Markov")
    self.assertContains(response, "Gizmo")

    # You can even inspect the context passed to the template.
    self.assertQuerysetEqual(
        response.context['cats'], ["<Cat: Gizmo>", "<Cat: Markov>"]
    )
