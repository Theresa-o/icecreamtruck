from django.contrib import admin

from .models import FoodItem, Inventory, Earnings, Transaction, Customer, FoodFlavor

admin.site.register(FoodItem)
admin.site.register(Inventory)
admin.site.register(Earnings)
admin.site.register(Transaction)
admin.site.register(Customer)
admin.site.register(FoodFlavor)