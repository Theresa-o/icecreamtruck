from pytest_factoryboy import register
from .factories import FoodItemFactory, FoodFlavorFactory, CustomerFactory

register(FoodItemFactory)
register(FoodFlavorFactory)
register(CustomerFactory)