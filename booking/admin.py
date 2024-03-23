from django.contrib import admin

import booking

# Register your models here.
from .models import Booking, Hotel_db, Room, Roomtype

admin.site.register(Hotel_db)
admin.site.register(Room)
admin.site.register(Roomtype)
admin.site.register(Booking)

