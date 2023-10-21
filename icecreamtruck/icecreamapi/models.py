from django.db import models

class FoodItem(models.Model):
    """
    Model representing a food item.

    This model is used to track different food items sold by the ice cream truck.

    Fields:
        name (str): The name of the food item.
        price (Decimal): The price of the food item.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
class FoodFlavor(models.Model):
    """
    Model representing a food item flavor.

    This model is used to represent flavors associated with food items.

    Fields:
        name (str): The name of the flavor.
        food_item (ForeignKey): The food item to which this flavor is associated.
    """
    name = models.CharField(max_length=100)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    """
    Model representing a customer.

    This model is used to store information about customers.

    Fields:
        name (str): The name of the customer.
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    """
    Model representing the inventory of food items.

    This model is used to track the quantity of food items available in the truck's inventory.

    Fields:
        food_item (ForeignKey): The food item being tracked in the inventory.
        food_quantity (PositiveIntegerField): The quantity of the food item in stock.
    """
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    food_quantity = models.PositiveIntegerField(default=0)

class Earnings(models.Model):
    """
    Model representing earnings for the ice cream truck.

    This model tracks the earnings of the ice cream truck.

    Fields:
        total_earnings (Decimal): The total earnings of the truck.
    """
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class Transaction(models.Model):
    """
    Model representing a customer's purchase transaction.

    This model is used to track individual purchase transactions made by customers.

    Fields:
        customer (ForeignKey): The customer making the purchase.
        food_item (ForeignKey): The food item being purchased.
        earnings (ForeignKey): The earnings record associated with this transaction.
        quantity (PositiveIntegerField): The quantity of the food item purchased.
        purchase_time (DateTimeField): The timestamp when the transaction was made.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    earnings = models.ForeignKey(Earnings, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)