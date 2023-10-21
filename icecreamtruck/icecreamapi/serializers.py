from rest_framework import serializers
from .models import FoodItem, FoodFlavor, Customer, Inventory

class FoodFlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodFlavor
        fields = "__all__"

class FoodItemSerializer(serializers.ModelSerializer):
    foodflavor = FoodFlavorSerializer(many=True, read_only=True)

    class Meta:
        model = FoodItem
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
