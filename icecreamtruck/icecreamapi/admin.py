from django.contrib import admin

from .models import FoodFlavor, FoodItem, Sale, Truck

admin.site.register(FoodItem)
admin.site.register(Sale)
admin.site.register(Truck)
admin.site.register(FoodFlavor)
