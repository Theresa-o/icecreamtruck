from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .models import FoodItem, Inventory, Earnings, Transaction
from .serializers import FoodItemSerializer, InventorySerializer, EarningsSerializer, TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing purchase transactions.

    This viewset allows you to create and retrieve purchase transactions.

    - To create a new transaction, send a POST request to this endpoint.
    - To retrieve a specific transaction, use a GET request.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the transaction being accessed.

    Returns:
        Response: A success message ("ENJOY!") or an error message ("SORRY!").
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=True, methods=['post'])
    def order(self, request, pk=None):
        food_item = self.get_object()
        purchase_quantity = request.data.get('quantity', 1)

        #check if the customer's purchase_quantity exceeds available stock
        if food_item.inventory.food_quantity < purchase_quantity:
            return Response("SORRY!", status=status.HTTP_400_BAD_REQUEST)
        
        # calculate the total cost of the customer's purchase
        total_cost = food_item.price * purchase_quantity

        # deduct the purchased quantity from inventory
        food_item.inventory.food_quantity -= purchase_quantity
        food_item.inventory.save() 

        # add the earnings from the sale
        try:
            earnings = Earnings.objects.get(pk=1)
            earnings.total_earnings += total_cost
        except:
            earnings = Earnings(total_earnings=total_cost)

        earnings.save()

        return Response("ENJOY!", status=status.HTTP_200_OK) 

class FoodItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing food items.

    This viewset allows you to create and retrieve food items.

    - To create a new food item, send a POST request to this endpoint.
    - To retrieve a list of food items or a specific food item, use a GET request.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the food item being accessed.

    Returns:
        Response: A Response object with food item details or an error message.
    """
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing food item inventory.

    This viewset allows you to create and retrieve inventory records.

    - To create a new inventory record, send a POST request to this endpoint.
    - To retrieve a list of inventory records or a specific inventory record, use a GET request.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the inventory record being accessed.

    Returns:
        Response: A Response object with inventory record details or an error message.
    """

    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class EarningsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing food truck earnings.

    This viewset allows you to create and retrieve earnings records.

    - To create a new earnings record, send a POST request to this endpoint.
    - To retrieve a list of earnings records or a specific earnings record, use a GET request.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the earnings record being accessed.

    Returns:
        Response: A Response object with earnings record details or an error message.
    """

    queryset = Earnings.objects.all()
    serializer_class = EarningsSerializer
