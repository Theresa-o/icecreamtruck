from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status
from django.contrib.auth.models import User
from icecreamtruck.icecreamapi.models import FoodFlavor, FoodItem, Sale, Truck
from icecreamtruck.test_settings import common_settings


@common_settings
class PurchaseViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.truck = Truck.objects.create(name='Test Truck')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.food_item = FoodItem.objects.create(
            name='Ice Cream', price=5.00, quantity=10, item_type='ice_cream', truck=self.truck
        )

    def test_create_purchase(self):
        response = self.client.post(reverse('purchase-list'), data={'food_id': self.food_item.id, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'ENJOY!'})

    def test_create_purchase_insufficient_quantity(self):
        response = self.client.post(reverse('purchase-list'), data={'food_id': self.food_item.id, 'quantity': 20})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'message': 'SORRY!'})

    def test_create_purchase_invalid_data(self):
        # Test with invalid data, missing food_id, or negative quantity
        response = self.client.post(reverse('purchase-list'), data={'quantity': -1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_purchase_food_not_found(self):
        # Test when the food item does not exist
        response = self.client.post(reverse('purchase-list'), data={'food_id': 999, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@common_settings
class InventoryViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.truck = Truck.objects.create(name='Test Truck')

    def test_list_inventory(self):
        response = self.client.get(reverse('inventory-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@common_settings
class TruckViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.truck = Truck.objects.create(name='Test Truck')
        self.truck1 = Truck.objects.create(name='Truck 1')
        self.truck2 = Truck.objects.create(name='Truck 2')

    def test_list_trucks(self):
        response = self.client.get(reverse('truck-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_truck(self):
        response = self.client.get(reverse('truck-detail', kwargs={'pk': self.truck.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_trucks(self):
        response = self.client.get(reverse('truck-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        trucks_data = response.data

        # Check if the response data is a list
        self.assertIsInstance(trucks_data, list)

        # Check the number of trucks in the response
        self.assertEqual(len(trucks_data), 3)

        # Check the structure of each truck data
        for truck_data in trucks_data:
            self.assertIn('id', truck_data)
            self.assertIn('name', truck_data)

@common_settings
class CreateTruckViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_truck(self):
        response = self.client.post(reverse('create-truck'), data={'name': 'New Truck'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'Ice cream truck created successfully.'})

    def test_create_truck_missing_name(self):
        response = self.client.post(reverse('create-truck'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

@common_settings
class CreateFoodItemViewSetTest(APITestCase):
    def setUp(self):
        self.truck = Truck.objects.create(name='Test Truck')
        self.url = reverse('create-food-item', args=[self.truck.id])

    def test_create_food_item_valid_data(self):
        valid_data = [
            {
                'name': 'Ice Cream',
                'price': '5.00',
                'quantity': 10,
                'item_type': 'ice_cream',
                'flavor': 'chocolate',
            },
            {
                'name': 'Shaved Ice',
                'price': '4.50',
                'quantity': 15,
                'item_type': 'shaved_ice',
                'flavor': 'pistachio',
            },
        ]
        response = self.client.post(self.url, valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Ensure food items and flavors were created
        self.assertEqual(FoodItem.objects.count(), len(valid_data))
        self.assertEqual(response.data['message'], 'Food items added successfully.')


    def test_create_food_item_invalid_data(self):
        invalid_data = [
            {
                'name': 'Snack',
                'price': '2.50',
                'quantity': 5,
                'item_type': 'InvalidType',
                'flavor': 'InvalidFlavor',
            },
            {
                'name': 'Invalid Food',
                'price': '3.00',
                'quantity': 0,  # Invalid quantity
                'item_type': 'snack_bar',
                'flavor': 'chocolate',
            },
        ]
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Ensure no food items and flavors were created due to validation errors
        self.assertEqual(FoodItem.objects.count(), 0)