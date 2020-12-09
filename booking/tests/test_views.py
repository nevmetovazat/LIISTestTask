import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ..models import Booking, Room
from ..serializers import BookingSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

username = 'nevmetovazat'
mail = 'nevmetov.azat@gmail.com'
password = 'very_secure_password'



class GetSingleBookingTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username, mail, password)
        self.client.login(username=username, password=password)
        response = self.client.post(reverse('authentication:token_obtain_pair'), data={
            'username':username, 'password': password})
        self.token = response.data['access']
        self.headers = {'HTTP_AUTHORIZATION': 'Bearer '+self.token}

        room = Room.objects.create(number=11, name='Переговорная')
        booking = Booking.objects.create(datetime_from='2020-12-01T12:00:00+0000',
            datetime_to='2020-12-01T19:00:00+0000',
            room=room,
            booked_by=user)
        self.booking_pk = booking.pk

    def test_get_single_booking(self):
        response = self.client.get(
            reverse(f'booking:default:bookings-detail', kwargs={'pk': self.booking_pk}),
            **self.headers
        )
        booking = Booking.objects.get(pk=self.booking_pk)
        serializer = BookingSerializer(booking)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

class CreateBookingTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username, mail, password)
        self.client.login(username=username, password=password)
        response = self.client.post(reverse('authentication:token_obtain_pair'), data={
            'username': username, 'password': password})
        self.token = response.data['access']
        self.headers = {'HTTP_AUTHORIZATION': 'Bearer ' + self.token}

        self.room = Room.objects.create(number=11, name='Переговорная')
        self.booking = Booking.objects.create(datetime_from='2020-12-01T12:00:00+0000',
                                         datetime_to='2020-12-01T19:00:00+0000',
                                         room=self.room,
                                         booked_by=user)

    def test_valid_booking_creation(self):
        data = {
            'datetime_from': '2020-12-02T12:00:00+0000',
            'datetime_to': '2020-12-02T19:00:00+0000',
            'room': self.room.pk
        }
        response = self.client.post(
            reverse(f'booking:default:bookings-list'),
            **self.headers, data=data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_booking_creation(self):
        """дата брони пересекается с датой другой брони"""
        data = {
            'datetime_from': '2020-12-01T12:00:00+0000',
            'datetime_to': '2020-12-01T20:00:00+0000',
            'room': self.room.pk
        }
        response = self.client.post(
            reverse(f'booking:default:bookings-list'),
            **self.headers, data=data, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)