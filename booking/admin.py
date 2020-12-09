from django.contrib import admin
from .models import Room, Booking

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
