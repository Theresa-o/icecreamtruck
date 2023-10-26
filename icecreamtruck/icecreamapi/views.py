from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import FoodFlavor, FoodItem, Sale, Truck
from .serializers import (CreateFoodItemSerializer, CreateTruckSerializer, PurchaseSerializer, TruckSerializer, SaleSerializer)

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

    # def list(self, request):
    #     # Retrieve the purchase history
    #     purchase_history = Sale.objects.filter(user=request.user).order_by('-purchase_time')
    #     purchase_history_serializer = SaleSerializer(purchase_history, many=True)

    #     # Retrieve the current purchase (if any) in the session
    #     current_purchase = request.session.get('current_purchase', {})

    #     return Response({
    #         'purchase_history': purchase_history_serializer.data,
    #         'current_purchase': current_purchase,
    #     }, status=status.HTTP_200_OK)

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
        
        #check if the customer's purchase_quantity exceeds available stock
        if food_item.quantity < quantity:
            return Response({'message': 'SORRY!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # deduct the purchased quantity from inventory
        food_item.quantity-=quantity
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
        serializer = CreateTruckSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        truck_name = serializer.validated_data['name']
        Truck.objects.create(name=truck_name)
        return Response({'message': 'Ice cream truck created successfully.'}, status=status.HTTP_201_CREATED)
    
class CreateFoodItemViewset(viewsets.ViewSet):
    """
    API endpoint for updating food items in an ice cream truck.

    This endpoint allows users to add new food items to a specific ice cream truck.

    Expects a PUT request with a JSON body containing the data for the new food items.
    """
    
    def create_food_item(self, request, truck_id):
        truck = get_object_or_404(Truck, id=truck_id)
        serializer = CreateFoodItemSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        food_items = serializer.validated_data

        for food_item_data in food_items:
            # ensure the food item is associated with the current truck
            food_item_data['truck'] = truck
            food_item = FoodItem.objects.create(**food_item_data)
            # check if the flavor is valid and create flavor object
            FoodFlavor.objects.create(name=food_item_data['food_flavor'], ice_cream=food_item)
        return Response({'message': 'Food items added successfully'}, status=status.HTTP_201_CREATED)













# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework import status
# from django.db.models import F
# from .models import FoodItem, Inventory, Earnings, Transaction
# from .serializers import FoodItemSerializer, InventorySerializer, EarningsSerializer, TransactionSerializer

# class TransactionViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for managing purchase transactions.

#     This viewset allows you to create and retrieve purchase transactions.

#     - To create a new transaction, send a POST request to this endpoint.
#     - To retrieve a specific transaction, use a GET request.

#     Parameters:
#         request (HttpRequest): The HTTP request object.
#         pk (int): The primary key of the transaction being accessed.

#     Returns:
#         Response: A success message ("ENJOY!") or an error message ("SORRY!").
#     """
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer

#     @action(detail=True, methods=['post'])
#     def order(self, request, pk=None):
#         food_item = self.get_object()
#         purchase_quantity = request.data.get('quantity', 1)

#         #check if the customer's purchase_quantity exceeds available stock
#         if food_item.inventory.food_quantity < purchase_quantity < 0:
#             return Response("SORRY!", status=status.HTTP_400_BAD_REQUEST)
        
#         # calculate the total cost of the customer's purchase
#         total_cost = food_item.price * purchase_quantity

#         # deduct the purchased quantity from inventory
#         food_item.inventory.food_quantity -= purchase_quantity
#         food_item.inventory.save() 

#         # add the earnings from the sale
#         try:
#             earnings = Earnings.objects.get(pk=1)
#             earnings.total_earnings += total_cost
#         except:
#             earnings = Earnings(total_earnings=total_cost)

#         earnings.save()

#         return Response("ENJOY!", status=status.HTTP_200_OK) 

# class FoodItemViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for managing food items.

#     This viewset allows you to create and retrieve food items.

#     - To create a new food item, send a POST request to this endpoint.
#     - To retrieve a list of food items or a specific food item, use a GET request.

#     Parameters:
#         request (HttpRequest): The HTTP request object.
#         pk (int): The primary key of the food item being accessed.

#     Returns:
#         Response: A Response object with food item details or an error message.
#     """
#     queryset = FoodItem.objects.all()
#     serializer_class = FoodItemSerializer

# class InventoryViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for managing food item inventory.

#     This viewset allows you to create and retrieve inventory records.

#     - To create a new inventory record, send a POST request to this endpoint.
#     - To retrieve a list of inventory records or a specific inventory record, use a GET request.

#     Parameters:
#         request (HttpRequest): The HTTP request object.
#         pk (int): The primary key of the inventory record being accessed.

#     Returns:
#         Response: A Response object with inventory record details or an error message.
#     """

#     queryset = Inventory.objects.all()
#     serializer_class = InventorySerializer

# class EarningsViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint for managing food truck earnings.

#     This viewset allows you to create and retrieve earnings records.

#     - To create a new earnings record, send a POST request to this endpoint.
#     - To retrieve a list of earnings records or a specific earnings record, use a GET request.

#     Parameters:
#         request (HttpRequest): The HTTP request object.
#     Returns:
#         Response: A Response object with earnings record details or an error message.
#     """

#     queryset = Earnings.objects.all()
#     serializer_class = EarningsSerializer
