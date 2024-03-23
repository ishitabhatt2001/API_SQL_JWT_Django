import jwt
from rest_framework import  status
from rest_framework.response import Response
from Project import settings
from .models import Booking, Room

def viewbookings(user_id):

    bookings = Booking.objects.filter(user_id=user_id)
    if Booking:
        return bookings
    
    else :
        return "Bookings not found"

def authorize(request):
    # Parse the authentication token from the request headers
        authorization_header = request.headers.get('Authorization', '')
        if not authorization_header.startswith('Bearer '):
            return None,False

        auth_token = authorization_header.split(' ')[1]
        if not auth_token:
            Response({'error': "noo token provided"})

        try:
            decoded_token = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
        except jwt.ExpiredSignatureError:
            return None,False
        except jwt.InvalidTokenError:
            return None,False
        
        return user_id,True
    
def change_room_status(room_id):
    try:
        room = Room.objects.get(id=room_id)
        if room.status == 'booked':
            return False  # Room is already booked
        room.status = 'booked'
        room.save()
        return True
    except Room.DoesNotExist:
        return False