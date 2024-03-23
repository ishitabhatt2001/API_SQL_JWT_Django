from django.urls import path
from .views import BookingCreateView, BookingDeleteAPIView, BookingListCreateAPIView, RoomWithRoomtypeListAPIView, bookingView
from .views2 import (
    booking_view,
    booking_list,
    room_with_roomtype_list,
    booking_create_view,
    booking_delete_view,
)

urlpatterns = [
    path('bookings/', BookingListCreateAPIView.as_view(), name='booking-list'),#api to view bookings
    path('rooms/', RoomWithRoomtypeListAPIView.as_view(), name='room-list'),#api to view rooms
    path('CreateBookings/', BookingCreateView.as_view(), name='booking-create'),#api to create a booking
    path('bookings/delete/', BookingDeleteAPIView.as_view(), name='booking-delete'),#api to delete a booking
    path('bookingview/', bookingView.as_view(), name='booking-view'),#simple APIView to view bookings
    path('booking2/', booking_view, name='booking-view'),
    path('booking/list-create2/', booking_list, name='booking-list-create'),
    path('room2/', room_with_roomtype_list, name='room-with-roomtype-list'),
    path('booking/create2/', booking_create_view, name='booking-create'),
    path('booking/delete2/', booking_delete_view, name='booking-delete'),
]
