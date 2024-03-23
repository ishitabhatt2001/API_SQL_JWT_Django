from django.http import JsonResponse
from Project import settings
from User.serializers import UserSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_id': user.id,  # Optionally, you can include the user's ID in the response
    }, status=status.HTTP_201_CREATED) 

def user_list(request):
    #get list ,serialize, return json
    user=user.objects.all()    
    serializer=UserSerializer(user, many=True)
    return Response({"users":serializer.data},status=status.HTTP_200_OK)


def delete_user( user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if not (user.is_staff_member or user.is_superuser):
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "User is a staff member or superuser and cannot be deleted"}, status=status.HTTP_403_FORBIDDEN)
    except user.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)