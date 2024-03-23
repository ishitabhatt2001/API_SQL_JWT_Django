
from django.http import JsonResponse
from Project import settings
from django.contrib.auth import authenticate,login
from .user import  delete_user, generate_tokens, user_list
from .permissions import IsAdmin, IsUser
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class UserView(APIView):
    permission_classes= [IsAuthenticated,IsAdmin]
    
    def get(self, request):
        return user_list(request)
    
    
def example_view(request):
    # Check if the request has the 'is_admin' attribute set by the middleware
    if hasattr(request, 'is_admin') and request.is_admin:
        response_data = {'message': 'You are an admin user.'}
    else:
        response_data = {'message': 'You are not an admin user.'}
    
    return JsonResponse(response_data)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request):
        # Include password in the request data
        data = request.data.copy()
        password = data.pop('password', None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Set password for the user
        if password:
            user.set_password(password)
            user.save()
        # Generate tokens
        return generate_tokens(user)
        
        

class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Validate email and password
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user=authenticate(request,email=email, password=password)
        login(request, user)
        return generate_tokens(user)
        


#for updating password
class UpdateUser(APIView):
    permission_classes = [IsAuthenticated,IsUser]
    def post(self, request):
        data = request.data.copy()
        password = data.pop('password', None)
        email = data.pop('email', None)
        new_password = data.pop('password', None)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Ensure both email and password are provided
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'New password is required'}, status=status.HTTP_400_BAD_REQUEST)

    

class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsUser]
    
    def delete(self, request):
        id=request.user.id
        return delete_user(id)
            
    