from django.test import TransactionTestCase
from django.db.utils import IntegrityError

from pizzastore.models import (
    Pizza,
    PizzaTopping,
    Topping,
)


class TestPizza(TransactionTestCase):

    def setUp(self):
        # Configure toppings
        self.cheese = Topping.objects.create(name="Cheese")
        self.ham = Topping.objects.create(name="Ham")
        self.pepperoni = Topping.objects.create(name="Pepperoni")
        self.mushrooms = Topping.objects.create(name="Mushrooms")
        self.onions = Topping.objects.create(name="Onions")
        self.garlic = Topping.objects.create(name="Garlic")
        self.pineapple = Topping.objects.create(name="Pineapple")

    def test_anchovies_are_not_a_valid_topping(self):
        with self.assertRaises(IntegrityError):
            Topping.objects.create(name="Anchovies")

    def test_cannot_have_multiple_of_the_same_topping(self):
        django_double = Pizza.objects.create(name="Django Double")
        PizzaTopping.objects.create(pizza=django_double, topping=self.cheese)
        # Adding the same topping again
        with self.assertRaises(IntegrityError):
            PizzaTopping.objects.create(pizza=django_double, topping=self.cheese)

    def test_max_five_toppings_on_a_pizza(self):
        django_special = Pizza.objects.create(name="Django Special")
        PizzaTopping.objects.create(pizza=django_special, topping=self.cheese)
        PizzaTopping.objects.create(pizza=django_special, topping=self.ham)
        PizzaTopping.objects.create(pizza=django_special, topping=self.pepperoni)
        PizzaTopping.objects.create(pizza=django_special, topping=self.mushrooms)
        PizzaTopping.objects.create(pizza=django_special, topping=self.onions)
        # Adding a 6th topping
        with self.assertRaises(IntegrityError):
            PizzaTopping.objects.create(pizza=django_special, topping=self.garlic)

    def test_no_pineapple_on_pizza(self):
        django_invalid = Pizza.objects.create(name="Django Invalid")
        # Adding pineapple
        with self.assertRaises(IntegrityError):
            PizzaTopping.objects.create(pizza=django_invalid, topping=self.pineapple)

