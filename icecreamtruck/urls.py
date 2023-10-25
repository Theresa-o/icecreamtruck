from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from icecreamtruck.icecreamapi import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
# router.register(r"FoodItem", views.FoodItemViewSet)
# router.register(r"Inventory", views.InventoryViewSet)
# router.register(r"Earnings", views.EarningsViewSet)
# router.register(r"Transaction", views.TransactionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs", SpectacularSwaggerView.as_view(url_name="schema"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
