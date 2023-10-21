from rest_framework import serializers
from .models import FoodItem, FoodFlavor, Customer, Inventory, Transaction, Earnings

class FoodFlavorSerializer(serializers.ModelSerializer):
    """
    Serializer for the FoodFlavor model.

    This serializer is used for serializing food item flavors.

    Fields:
        All fields from the FoodFlavor model.
    """

    class Meta:
        model = FoodFlavor
        fields = "__all__"

class FoodItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the FoodItem model.

    This serializer is used for serializing food items and their associated flavors.

    Fields:
        All fields from the FoodItem model.
    """

    foodflavor = FoodFlavorSerializer(many=True, read_only=True)

    class Meta:
        model = FoodItem
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.

    This serializer is used for serializing customer data.

    Fields:
        All fields from the Customer model.
    """

    class Meta:
        model = Customer
        fields = "__all__"

class InventorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Inventory model.

    This serializer is used for serializing inventory data.

    Fields:
        All fields from the Inventory model.
    """

    class Meta:
        model = Inventory
        fields = "__all__"

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    This serializer is used for serializing purchase transactions made by customers.

    Fields:
        All fields from the Transaction model.
    """

    class Meta:
        model = Transaction
        fields = "__all__"

class EarningsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Earnings model.

    This serializer is used for serializing earnings data.

    Fields:
        All fields from the Earnings model.
    """

    class Meta:
        model = Earnings
        fields = "__all__"
