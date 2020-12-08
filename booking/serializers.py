from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from .models import Booking, Room

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'name')


class BookingSerializer(serializers.ModelSerializer):
    datetime_from = serializers.DateTimeField(required=True)
    datetime_to = serializers.DateTimeField(required=True)
    room = serializers.PrimaryKeyRelatedField(required=True, queryset=Room.objects.all())
    booked_by = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Booking
        fields = ('datetime_from', 'datetime_to', 'room', 'booked_by')

    def validate(self, attrs):
        """Проверяет для одной комнаты:
        datetime_from пересекается с другой датой брони
        datetime_to пересекается с другой датой брони
        """

        intersected_bookings = Booking.objects.filter(Q(room=attrs['room']) &
                                                    ((Q(datetime_from__lte=attrs['datetime_from']) & Q(
                                                        datetime_to__gte=attrs['datetime_from']))
                                                     |
                                                     (Q(datetime_from__lte=attrs['datetime_to']) & Q(
                                                         datetime_to__gte=attrs['datetime_to'])))
                                                    )
        if intersected_bookings.first() is not None:
            raise ValidationError(f'Бронь на номер с id={intersected_bookings.first().pk} пересекается с указанными датами')
        else:
            return attrs