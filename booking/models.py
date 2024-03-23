from django.db import models
from django.conf import settings
 
 
class Booking(models.Model):
    id=models.BigAutoField(primary_key=True)
    roomno = models.CharField(blank=True, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    total_price = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'booking_db'
        
    def __str__(self):
        return str(self.id)
        
        
class Hotel_db(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    staff_user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True, null=True, related_name='hotels', limit_choices_to={'is_staff_member': True})
    phone_number = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'hotel_db'
        
        
    def __str__(self):
        return self.name

class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    hotel = models.ForeignKey('Hotel_db', models.DO_NOTHING, blank=True, null=True)
    typeid = models.ForeignKey('Roomtype', on_delete=models.CASCADE,db_column='type_id', blank=True, null=True)
    status = models.CharField(blank=True, null=True)
    roomno = models.CharField(blank=True, null=True)
    descriptionn = models.CharField(blank=True, null=True)
    price_per_night = models.BigIntegerField(blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'room_db'
        
    def __str__(self):
        return str(self.id)


class Roomtype(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roomtype_db'
        
    def __str__(self):
        return self.name
