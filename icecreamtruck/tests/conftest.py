from pytest_factoryboy import register

from .factories import CustomerFactory, FoodFlavorFactory, FoodItemFactory

register(FoodItemFactory)
register(FoodFlavorFactory)
register(CustomerFactory)
