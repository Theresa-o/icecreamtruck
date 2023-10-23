import factory
from icecreamtruck.icecreamapi.models import FoodItem, FoodFlavor, Customer

class FoodItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodItem

    name = "test_fooditem"
    price = 5.00

class FoodFlavorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FoodFlavor

    name = "test_foodflavor"
    food_item = factory.SubFactory(FoodItemFactory)

class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer

    name = "test_customer"