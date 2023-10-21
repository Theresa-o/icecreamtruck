from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
class FoodFlavor(models.Model):
    name = models.CharField(max_length=100)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Inventory(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    food_quantity = models.PositiveIntegerField(default=0)
