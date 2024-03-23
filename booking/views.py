from urllib import response
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics,status
from rest_framework.response import Response
from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer
from .booking import authorize, change_room_status, viewbookings

#using normal APIView
class bookingView(APIView):
    def get(self,request):
        id=request.user.id
        bookingView = viewbookings(id)
        if bookingView:
            serializer = BookingSerializer(bookingView,many=True)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "invalid token"}, status=status.HTTP_404_NOT_FOUND)

#bookin view using listAPIView
class BookingListCreateAPIView(generics.ListAPIView):

    serializer_class = BookingSerializer
    def get_queryset(self,request):
        id=request.user.id
        return Booking.objects.filter(user_id=id)


#room view for all available rooms
class RoomWithRoomtypeListAPIView(generics.ListAPIView):
    queryset = Room.objects.filter(status='available').select_related('typeid')
    serializer_class = RoomSerializer


#create a booking
class BookingCreateView(generics.CreateAPIView):
    serializer_class = BookingSerializer

    def create(self, request):
        # Add the user to the request data
        id=request.user.id
        request_data = request.data.copy()
     # Assuming user is authenticated
        room_id = request_data.pop('room', None)
        if room_id:
            if change_room_status(room_id):
                serializer = self.get_serializer(data=request_data)
                serializer.is_valid(raise_exception=True)
                serializer.save(user_id=id)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"error": "Room not found/ is already booked"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Room ID not provided"}, status=status.HTTP_400_BAD_REQUEST)




#delete a booking
class BookingDeleteAPIView(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def delete(self, request):
        # Get the user ID from the URL kwargs
        id=request.user.id
        data = request.data.copy()
        roomno = data.pop('roomno', None)
        
        
        # Validate that both user_id and roomno are provided
        if not roomno:
            return Response({"error": "Both user_id and roomno must be provided "}, status=status.HTTP_400_BAD_REQUEST)
        

            # Filter bookings by user ID and room number
            
        bookings = self.get_queryset().filter(user_id=id, roomno=roomno)

        # Check if the bookings exist
        if not bookings.exists():
            return Response({"error": "Bookings not found"}, status=status.HTTP_404_NOT_FOUND)

        # Loop through each booking
        for booking in bookings:
            # Get the associated room and update its status
            room = booking.room
            room.status = 'available'
            room.save()

            # Delete the booking
            booking.delete()
