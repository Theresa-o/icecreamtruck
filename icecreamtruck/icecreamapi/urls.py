from django.urls import include, path

from .views import (
    CreateFoodItemViewset,
    CreateTruckViewSet,
    FoodItemViewSet,
    InventoryViewSet,
    PurchaseViewSet,
    TruckViewSet,
)

urlpatterns = [
    path('purchase/', PurchaseViewSet.as_view({'post': 'create'}), name='purchase-list'),
    path('inventory/', InventoryViewSet.as_view({'get': 'list'}), name='inventory-list'),
    path('fooditem/', FoodItemViewSet.as_view({'get': 'list'}), name='fooditem-list'),
    path('fooditem/<int:pk>/', FoodItemViewSet.as_view({'get': 'retrieve'}), name='fooditem-detail'),
    path('trucks/', TruckViewSet.as_view({'get': 'list'}), name='truck-list'),
    path('trucks/<int:pk>/', TruckViewSet.as_view({'get': 'retrieve'}), name='truck-detail'),
    path('trucks/create/', CreateTruckViewSet.as_view({'post': 'create'}), name='create-truck'),
    path(
        'trucks/<int:truck_id>/create-food-item/<str:flavour>/',
        CreateFoodItemViewset.as_view({'post': 'create'}),
        name='create-food-item',
    ),
]
