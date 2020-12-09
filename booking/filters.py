from django_filters import FilterSet, DateTimeFilter

from .models import Booking, Room


class BookingFilter(FilterSet):
    datetime_from = DateTimeFilter(field_name='datetime_from', lookup_expr='gt')
    datetime_to = DateTimeFilter(field_name='datetime_to', lookup_expr='lt')

    class Meta:
        model = Booking
        fields = ('datetime_from', 'datetime_to', 'room', 'booked_by')


class RoomFilter(FilterSet):
    datetime_from = DateTimeFilter(field_name='booking__datetime_from', lookup_expr='gte')
    datetime_to = DateTimeFilter(field_name='booking__datetime_to', lookup_expr='lte')

    class Meta:
        model = Room
        fields = ('datetime_from', 'datetime_to')
