from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FoodItem, FoodFlavor, Truck, Sale

class FoodFlavorSerializer(serializers.ModelSerializer):
    """
    This serializer is used for serializing food item flavors.
    """

    class Meta:
        model = FoodFlavor
        fields = ["name", "food_item"]     


class FoodItemSerializer(serializers.ModelSerializer):
    """
    This serializer is used for serializing food items and their associated flavors.
    """
    
    class Meta:
        model = FoodItem
        fields = ["name", "price", "quantity", "item_type", "image"]

class UserSerializer(serializers.ModelSerializer):
    """
    This serializer is used for serializing customer data.
    """

    class Meta:
        model = User
        fields = ["username", "email"]

class TruckSerializer(serializers.ModelSerializer):
    """
    Serializer for truck model.
    """

    total_sales = serializers.SerializerMethodField()
    food_items = FoodItemSerializer(many=True)

    class Meta:
        model = Truck
        fields = ["id", "name", "food_items", "total_sales"]

    def get_total_sales(self, obj):
        return obj.total_sales()

class PurchaseSerializer(serializers.Serializer):

    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer")
        return value
    
class CreateTruckSerializer(serializers.Serializer):
    # creating a new truck 
    name = serializers.CharField(max_length=100, required=True)

class CreateFoodItemSerializer(serializers.ModelSerializer):
    # add a field for flavour
    # flavor = serializers.CharField(max_length=2, required=True)
    food_flavor = serializers.CharField(max_length=20)

    class Meta:
        model = FoodItem
        fields = ["name", "price", "quantity", "item_type", "food_flavor", "image", "truck"]

    def validate_item_type(self, value):
        # validate the food item type field to ensure that it matches with the choices in the model
        valid_choices = [choice[0] for choice in FoodItem.ITEM_TYPES]

        if value not in valid_choices:
            raise serializers.ValidationError(f"'item_type' must be one of {valid_choices}")

    def validate_food_flavor(self, value):
        # validate the food flavor field to ensure that it matches with the choices in the model
        valid_choices = [choice[0] for choice in FoodFlavor.FLAVORS]

        if value not in valid_choices:
            raise serializers.ValidationError(f"'food_flavor' must be one of {valid_choices}")
        return value
    
class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sale model.

    """

    class Meta:
        model = Sale
        fields = ["truck", "food_item", "user", "quantity", "purchase_time"]


# class InventorySerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Inventory model.

#     This serializer is used for serializing inventory data.

#     Fields:
#         All fields from the Inventory model.
#     """

#     class Meta:
#         model = Inventory
#         fields = "__all__"

# class TransactionSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Transaction model.

#     This serializer is used for serializing purchase transactions made by customers.

#     Fields:
#         All fields from the Transaction model.
#     """

#     class Meta:
#         model = Transaction
#         fields = "__all__"

# class EarningsSerializer(serializers.ModelSerializer):
#     """
#     Serializer for the Earnings model.

#     This serializer is used for serializing earnings data.

#     Fields:
#         All fields from the Earnings model.
#     """

#     class Meta:
#         model = Earnings
#         fields = "__all__"
