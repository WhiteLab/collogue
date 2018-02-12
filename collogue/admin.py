from django.contrib import admin

from collogue.models import Room, Reservation

# Register your models here.
admin.site.register(Room)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'approved')