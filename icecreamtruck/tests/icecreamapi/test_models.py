import pytest

# Access to the database for the test
pytestmark = pytest.mark.django_db

# test the return value of the __str__ method
class TestFoodItemModel:
    def test_str_method(self, food_item_factory):
        item = food_item_factory()
        assert item.__str__() == "test_fooditem"

# test the return value of the __str__ method
class TestFoodFlavorModel:
    def test_str_method(self, food_flavor_factory):
        item = food_flavor_factory()
        assert item.__str__() == "test_foodflavor"

# test the return value of the __str__ method
class TestCustomerModel:
    def test_str_method(self, customer_factory):
        item = customer_factory()
        assert item.__str__() == "test_customer"
