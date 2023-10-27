from django.test import TestCase
from django.contrib.auth.models import User
from icecreamtruck.icecreamapi.models import FoodFlavor, FoodItem, Sale, Truck

class TruckModelTest(TestCase):
    def setUp(self):
        self.truck = Truck.objects.create(name='Test Truck')

    def test_truck_creation(self):
        self.assertEqual(self.truck.name, 'Test Truck')

    def test_total_sales_method(self):
        # Create a test user
        user = User.objects.create_user(username='testuser', password='testpassword')  

        food_item = FoodItem.objects.create(
            name='Ice Cream',
            price=5.00,
            quantity=10,
            item_type='ice_cream',
            truck=self.truck,
        )
        Sale.objects.create(food_item=food_item, truck=self.truck, user=user, quantity=2)

        print(f"Debug: truck.sales.all() returns {self.truck.sales.all()}")
        print(f"Debug: total_sales() returned {self.truck.total_sales()}")
        print(f"Debug: Current truck name: {self.truck.name}")

        self.assertEqual(self.truck.total_sales(), 10.00)

        food_item_1 = FoodItem.objects.create(
            name='Shaved Ice',
            price=10.00,
            quantity=5,
            item_type='shaved_ice',
            truck=self.truck,
        )

        Sale.objects.create(food_item=food_item_1, truck=self.truck, user=user, quantity=1)

        self.assertEqual(self.truck.total_sales(), 20.00)


class FoodItemModelTest(TestCase):
    def setUp(self):
        self.truck = Truck.objects.create(name='Test Truck')
        self.food_item = FoodItem.objects.create(
            name='Ice Cream', price=5.00, quantity=10, item_type='ice_cream', truck=self.truck
        )

    def test_food_item_creation(self):
        self.assertEqual(self.food_item.name, 'Ice Cream')
        self.assertEqual(self.food_item.price, 5.00)
        self.assertEqual(self.food_item.quantity, 10)
        self.assertEqual(self.food_item.item_type, 'ice_cream')
        self.assertEqual(self.food_item.truck, self.truck)

class FlavorModelTest(TestCase):
    def setUp(self):
        self.truck = Truck.objects.create(name='Test Truck')
        self.food_item = FoodItem.objects.create(
            name='Ice Cream', price=5.00, quantity=10, item_type='ice_cream', truck=self.truck
        )
        self.flavor = FoodFlavor.objects.create(name='chocolate', food_item=self.food_item)

    def test_flavor_creation(self):
        self.assertEqual(self.flavor.name, 'chocolate')
        self.assertEqual(self.flavor.food_item, self.food_item)

class SaleModelTest(TestCase):
    def setUp(self):
        self.truck = Truck.objects.create(name='Test Truck')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.food_item = FoodItem.objects.create(
            name='Ice Cream', price=5.00, quantity=10, item_type='ice_cream', truck=self.truck
        )
        self.sale = Sale.objects.create(food_item=self.food_item, truck=self.truck, user=self.user, quantity=2)

    def test_sale_creation(self):
        self.assertEqual(self.sale.food_item, self.food_item)
        self.assertEqual(self.sale.truck, self.truck)
        self.assertEqual(self.sale.user, self.user)
        self.assertEqual(self.sale.quantity, 2)