from rest_framework import serializers
from .models import Booking, Room

class BookingSerializer(serializers.ModelSerializer):
    from_date = serializers.DateField(format='%Y-%m-%d')
    to_date = serializers.DateField(format='%Y-%m-%d')


    class Meta:
        model = Booking
        fields = [ 'roomno', 'from_date', 'to_date', 'total_price', 'user', 'room']
        extra_kwargs = {
            field_name: {'required': True}
            for field_name in model._meta.fields  # Setting all fields as required
        }

class RoomSerializer(serializers.ModelSerializer):
    roomtype_name = serializers.CharField(source='typeid.name', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
