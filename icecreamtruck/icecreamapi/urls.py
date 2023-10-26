from django.urls import include, path

from .views import CreateFoodItemViewset, CreateTruckViewSet, InventoryViewSet, PurchaseViewSet, TruckViewSet

urlpatterns = [
    path('purchase/', PurchaseViewSet.as_view({'post': 'create'}), name='purchase-list'),
    path('inventory/', InventoryViewSet.as_view({'get': 'list'}), name='inventory-list'),
    path('trucks/', TruckViewSet.as_view({'get': 'list'}), name='truck-list'),
    path('trucks/<int:pk>/', TruckViewSet.as_view({'get': 'retrieve'}), name='truck-detail'),
    path('trucks/create/', CreateTruckViewSet.as_view({'post': 'create'}), name='create-truck'),
    path(
        'trucks/<int:truck_id>/create-food-item/',
        CreateFoodItemViewset.as_view({'post': 'create_food_item'}),
        name='create-food-item',
        ),

]