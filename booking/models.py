from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class Room(models.Model):
    number = models.PositiveIntegerField(null=False, blank=False, unique=True, verbose_name='Номер комнаты')
    name = models.CharField(max_length=64, null=False, blank=False, verbose_name='Имя комнаты')

    @property
    def bookings(self):
        return self.booking_set.all()


class Booking(models.Model):
    datetime_from = models.DateTimeField(verbose_name='Начало брони', null=False, blank=False)
    datetime_to = models.DateTimeField(verbose_name='Конец брони', null=False, blank=False)
    room = models.ForeignKey('Room', on_delete=models.PROTECT,
                             verbose_name='Забронированная комната')
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                  verbose_name='Пользователь, поставивший бронь')
