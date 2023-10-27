from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import FoodFlavor, FoodItem, Sale, Truck
from .serializers import (
    CreateFoodItemSerializer,
    CreateTruckSerializer,
    FoodItemSerializer,
    PurchaseSerializer,
    TruckSerializer,
)


class PurchaseViewSet(viewsets.ViewSet):
    """
    API endpoint for making a purchase from the ice cream truck.

    This endpoint allows customers to make a purchase from the ice cream truck by specifying
    the food item ID and the quantity they want to purchase.

    Expects a POST request with the following data:
    - 'food_id': The ID of the food item to purchase.
    - 'quantity': The quantity of the food item to purchase.

    If the food item is found and the quantity is available, the purchase is successful,
    and the response message is 'ENJOY!'. If the food item is not found, a 404 Not Found
    response is returned. If the quantity is not available, a 400 Bad Request response is
    returned with the message 'SORRY!'.
    """

    def create(self, request):
        serializer = PurchaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        food_id = serializer.validated_data['food_id']
        quantity = serializer.validated_data['quantity']

        # Confirm if food item is available
        try:
            food_item = FoodItem.objects.get(id=food_id)
        except FoodItem.DoesNotExist:
            return Response({'message': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

        # check if the customer's purchase_quantity exceeds available stock
        if food_item.quantity < quantity:
            return Response({'message': 'SORRY!'}, status=status.HTTP_400_BAD_REQUEST)

        # deduct the purchased quantity from inventory
        food_item.quantity -= quantity
        food_item.save()

        if request.user.is_authenticated:
            Sale.objects.create(food_item=food_item, truck=food_item.truck, user=request.user, quantity=quantity)
        else:
            Sale.objects.create(food_item=food_item, truck=food_item.truck, quantity=quantity)
        return Response({'message': "ENJOY!"}, status=status.HTTP_201_CREATED)


class InventoryViewSet(viewsets.ViewSet):
    """
    API endpoint for retrieving the trucks inventory.

    This endpoint returns a list of all ice cream trucks along with their inventory of food items
    and total sales.

    Expects a GET request without any data.

    Returns a JSON response containing information about the ice cream trucks, their food items,
    and total sales.
    """

    def list(self, request):
        trucks = TruckSerializer(Truck.objects.all(), many=True)
        return Response({'Inventory': trucks.data}, status=status.HTTP_200_OK)


class FoodItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing food items.

    This viewset allows you to retrieve food items.

    - To retrieve a list of food items or a specific food item, use a GET request.

    Returns:
        Response: A Response object with food item details or an error message.
    """

    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer


class TruckViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing ice cream trucks.

    This endpoint allows users to view a list of all ice cream trucks.

    Expects a GET request without any data.

    Returns a JSON response with a list of ice cream trucks and their details.
    """

    queryset = Truck.objects.all()
    serializer_class = TruckSerializer


class CreateTruckViewSet(viewsets.ViewSet):
    """
    API endpoint for creating a new ice cream truck.

    This endpoint allows users to create a new ice cream truck by providing a name for the truck.

    Expects a POST request with the following data:
    - 'name': The name of the new ice cream truck.

    If the name is provided, a new ice cream truck is created, and the response message is
    'Ice cream truck created successfully'. If the name is missing, a 400 Bad Request response
    is returned with the message 'Truck name is required.'.
    """

    def create(self, request):
        serializer = CreateTruckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        truck_name = serializer.validated_data['name']
        Truck.objects.create(name=truck_name)
        return Response({'message': 'Ice cream truck created successfully.'}, status=status.HTTP_201_CREATED)


class CreateFoodItemViewset(viewsets.ModelViewSet):
    """
    API endpoint for updating food items in an ice cream truck.

    This endpoint allows users to add new food items to a specific ice cream truck.

    Expects a PUT request with a JSON body containing the data for the new food items.
    """

    serializer_class = CreateFoodItemSerializer

    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        truck_id = self.kwargs['truck_id']
        flavour = self.kwargs['flavour']
        truck = get_object_or_404(Truck, id=truck_id)
        instance = serializer.save(truck=truck)
        FoodFlavor.objects.create(name=flavour, food_item=instance)
