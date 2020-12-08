from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, RoomViewSet

app_name = 'booking'

router = DefaultRouter()
router.register(r'bookings', BookingViewSet)
router.register(r'rooms', RoomViewSet)

urlpatterns = [
    url(r'^', include((router.urls, app_name), namespace='default'))
]