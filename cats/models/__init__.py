from django.db import transaction
from .cat import Cat
from .cat_human_relationship import CatHumanRelationship
from .human import Human
from .toy import Toy

@transaction.atomic
def create_initial_model_instances():
  markov = Cat(name="Markov", age=6)
  markov.save()

  curie = Cat(name="Curie", age=5)
  curie.save()

  christmas_tree = Toy(name="christmas tree", cat=markov)
  christmas_tree.save()

  mousey = Toy(name="mousey", cat=curie)
  mousey.save()

  ned = Human(
      username="ruggeri",
      is_superuser=True,
      is_staff=True,
  )
  ned.set_password("password")
  ned.save()

  CatHumanRelationship(
      cat=markov, human=ned, years_of_durations=6
  ).save()
  CatHumanRelationship(
      cat=curie, human=ned, years_of_durations=5
  ).save()
