from .booking import change_room_status, viewbookings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


@api_view(['GET'])
def booking_view(request):
    if request.method == 'GET':
        id=request.user.id
        booking = viewbookings(id)
        if booking:
            serializer = BookingSerializer(booking, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "invalid token"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def booking_list(request):
    if request.method == 'GET':
        id=request.user.id
        queryset = Booking.objects.filter(user_id=id)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def room_with_roomtype_list(request):
    if request.method == 'GET':
        queryset = Room.objects.filter(status='available').select_related('typeid')
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def booking_create_view(request):
    if request.method == 'POST':
        id=request.user.id
        request_data = request.data.copy()
        room_id = request_data.pop('room', None)
        if room_id:
            if change_room_status(room_id):
                serializer = BookingSerializer(data=request_data)
                if serializer.is_valid():
                    serializer.save(user_id=id)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Room not found/ is already booked"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Room ID not provided"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def booking_delete_view(request):
    if request.method == 'DELETE':
        id=request.user.id
        data = request.data.copy()
        roomno = data.pop('roomno', None)
        if not id or not roomno:
            return Response({"error": "Both user_id and roomno must be provided "}, status=status.HTTP_400_BAD_REQUEST)
        
        bookings = Booking.objects.filter(user_id=id, roomno=roomno)
        if not bookings.exists():
            return Response({"error": "Bookings not found"}, status=status.HTTP_404_NOT_FOUND)
        
        for booking in bookings:
            room = booking.room
            room.status = 'available'
            room.save()
            booking.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
