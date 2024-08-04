from profile import Profile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from clients.serializers import UserProfileSerializer
from .serializers import UserSerializer

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def register(request):
    user_data = request.data.copy()
    user_serializer = UserSerializer(data=user_data)

    if user_serializer.is_valid():
        # Create the user
        user = user_serializer.save()
        
        # Create a token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Prepare profile data
        profile_data = {
            "first_name": user_data.get('first_name', ''),
            "middle_name": user_data.get('middle_name', ''),
            "last_name": user_data.get('last_name', ''),
            "phone": user_data.get('phone', ''),
            "address_line1": user_data.get('address_line1', ''),
            "address_line2": user_data.get('address_line2', ''),
            "city": user_data.get('city', ''),
            "state": user_data.get('state', ''),
            "postcode": user_data.get('postcode', ''),
            "country": user_data.get('country', ''),
            "user": user.id  # Include the user ID
        }

        # Create the profile with the user field set
        profile_serializer = UserProfileSerializer(data=profile_data)

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({
                'token': token.key,
                'user': user_serializer.data,
                'profile': profile_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # If profile creation fails, delete the user and return errors
            user.delete()
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)