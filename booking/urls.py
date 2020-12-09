from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, RoomViewSet

app_name = 'booking'

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='bookings')
router.register(r'rooms', RoomViewSet, basename='rooms')

urlpatterns = [
    url(r'^', include((router.urls, app_name), namespace='default'))
]
