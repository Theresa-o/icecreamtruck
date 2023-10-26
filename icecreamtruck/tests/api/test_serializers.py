from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from icecreamtruck.icecreamapi.models import FoodFlavor, FoodItem, Sale, Truck
from icecreamtruck.icecreamapi.serializers import (FoodItemSerializer, UserSerializer, CreateFoodItemSerializer, CreateTruckSerializer, PurchaseSerializer, TruckSerializer, SaleSerializer)

# class FoodItemSerializer(TestCase):
#     def test_valid_serializer(self):
#         data = {
#             'name': 'Ice Cream',
#             'price': '5.00',
#             'quantity': 10,
#             'item_type': 'ice_cream',
#         }
#         serializer = FoodItemSerializer(data=data)
#         self.assertTrue(serializer.is_valid())

#     def test_invalid_serializer(self):
#         data = {
#             'name': 'Invalid Food Item',
#             'price': '-2.50',
#             'quantity': -10,
#             'food_type': 'InvalidType',
#         }
#         serializer = FoodItemSerializer(data=data)
#         self.assertFalse(serializer.is_valid())
# 

class FoodItemSerializerTest(TestCase):
    
    def test_valid_serializer(self):

        image_path = 'images/pistachio/pistachioicecream.jpg'

        # Open the image file and read its binary content
        with open(image_path, 'rb') as image_file:
            image_data = SimpleUploadedFile(os.path.basename(image_path), image_file.read(), content_type="image/jpeg")


        data = {
            'name': 'Ice Cream',
            'price': '5.00',
            'quantity': 10,
            'item_type': 'ice_cream',
            'image': image_data,
        }
        serializer = FoodItemSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self):
        image_path = 'images/pistachio/pistachioicecream.jpg'

        # Open the image file and read its binary content
        with open(image_path, 'rb') as image_file:
            image_data = SimpleUploadedFile(os.path.basename(image_path), image_file.read(), content_type="image/jpeg")

        data = {
            'name': 'Invalid Food Item',
            'price': '-2.50',
            'quantity': -10,
            'item_type': 'InvalidType',
            'image': image_data,
        }
        serializer = FoodItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class UserSerializerTest(TestCase):
    def test_user_serializer(self):
        user = User(username='testuser', email='test@example.com')
        serializer = UserSerializer(user)
        expected_data = {'username': 'testuser', 'email': 'test@example.com'}
        self.assertEqual(serializer.data, expected_data)

class TruckSerializerTest(TestCase):
    def test_valid_truck_serializer(self):
        truck = Truck.objects.create(id=1, name='Test Truck')
        food_item = FoodItem.objects.create(name='Ice Cream', price='5.00', quantity=10, item_type='ice_cream', truck=truck)
        serializer = TruckSerializer(truck)
        expected_data = {
            'id': 1,
            'name': 'Test Truck',
            'food_items': [FoodItemSerializer(food_item).data],
            'total_sales': 0,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_invalid_truck_serializer(self):
        truck = Truck(id=1, name='Invalid Truck')
        serializer = TruckSerializer(truck)
        self.assertEqual(serializer.data, {'id': 1, 'name': 'Invalid Truck', 'food_items': [], 'total_sales': 0})

class PurchaseSerializerTest(TestCase):
    def test_valid_purchase_serializer(self):
        data = {'food_id': 1, 'quantity': 5}
        serializer = PurchaseSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_purchase_serializer(self):
        data = {'food_id': 1, 'quantity': -5}
        serializer = PurchaseSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class CreateTruckSerializerTest(TestCase):
    def test_valid_create_truck_serializer(self):
        data = {'name': 'New Truck'}
        serializer = CreateTruckSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_create_truck_serializer(self):
        data = {'name': ''}
        serializer = CreateTruckSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class CreateFoodItemSerializerTest(TestCase):
    def test_valid_create_food_item_serializer(self):
        # Create a Truck object
        self.truck = Truck.objects.create(id=1, name='Test Truck')
        # Create an image path to populate test
        image_path = 'images/pistachio/pistachioicecream.jpg'

        # Open the image file and read its binary content
        with open(image_path, 'rb') as image_file:
            image_data = SimpleUploadedFile(os.path.basename(image_path), image_file.read(), content_type="image/jpeg")

        data = {
            'name': 'Ice Cream',
            'price': '5.00',
            'quantity': 10,
            'item_type': 'ice_cream',
            'flavor': 'chocolate',
            'image': image_data,
            'truck': self.truck.id,
        }
        serializer = CreateFoodItemSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        # self.assertTrue(serializer.is_valid())

    def test_invalid_create_food_item_serializer(self):
        # Create a Truck object
        self.truck = Truck.objects.create(id=1, name='Test Truck')
        # Create an image path to populate test
        image_path = 'images/pistachio/pistachioicecream.jpg'

        # Open the image file and read its binary content
        with open(image_path, 'rb') as image_file:
            image_data = SimpleUploadedFile(os.path.basename(image_path), image_file.read(), content_type="image/jpeg")

        data = {
            'name': 'Ice Cream',
            'price': '5.00',
            'quantity': 10,
            'item_type': 'InvalidType',
            'flavor': 'InvalidFlavor',
            'image': image_data,
            'truck': self.truck.id,
        }
        serializer = CreateFoodItemSerializer(data=data)
        self.assertFalse(serializer.is_valid())