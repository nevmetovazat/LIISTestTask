from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Booking, Room
from .filters import BookingFilter, RoomFilter
from .serializers import BookingSerializer, RoomSerializer

class BookingViewSet(viewsets.ModelViewSet):
    # queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = BookingFilter

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(booked_by=user)

class RoomViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]
    filterset_class = RoomFilter
