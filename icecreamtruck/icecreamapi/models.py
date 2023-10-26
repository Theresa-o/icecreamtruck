from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import F, Sum

class Truck(models.Model):
    """
    Ice Cream Truck model representing an ice cream truck.
    """

    # Add a reverse relationship to Sale
    sales = models.ManyToManyField('Sale', related_name='trucks', blank=True)

    name = models.CharField(max_length=100)

    def total_sales(self):
        sales = self.sales.annotate(total=F('food_item__price') * F('quantity'))
        total = sales.aggregate(total_sales=Sum('total'))['total_sales']
        return total if total else 0

    def __str__(self):
        return self.name
    
class FoodItem(models.Model):
    """

    This model is used to track different food items sold by the ice cream truck.
    """

    ITEM_TYPES = [
        ('ice_cream', 'Ice Cream'),
        ('shaved_ice', 'Shaved Ice'),
        ('snack_bar', 'Snack Bar'),
    ]
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPES,
        default='ice_cream',
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    truck = models.ForeignKey(Truck, related_name="food_items", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.get_item_type_display()}) - ${self.price}"
    
class FoodFlavor(models.Model):
    """

    This model is used to represent flavors associated with food items.

    """
    FLAVORS = [
        ('chocolate', 'Chocolate'),
        ('pistachio', 'Pistachio'),
        ('strawberry', 'Strawberry'),
        ('mint', 'Mint'),
    ]

    name = models.CharField(max_length=20, choices=FLAVORS)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
# class Inventory(models.Model):
#     """
#     This model is used to track the quantity of food items available in the truck's inventory.
#     """
#     food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
#     food_quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])

# class Earnings(models.Model):
#     """
#     This model tracks the earnings of the ice cream truck.
#     """
#     total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

class Sale(models.Model):
    """

    This model is used to track individual purchase transactions made by customers.

    """
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, related_name="sales", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_time = models.DateTimeField(auto_now_add=True)
    # earnings = models.ForeignKey(Earnings, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale of {self.quantity} x {self.food_item}"