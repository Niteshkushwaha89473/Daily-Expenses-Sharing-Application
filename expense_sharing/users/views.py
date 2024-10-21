from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.models import User
from .serializers import UserSerializer
import csv
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split()[1])
            user_from_token = jwt_authenticator.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        if user != user_from_token:
            raise AuthenticationFailed('Token does not match the requested user')

        return super().retrieve(request, *args, **kwargs)
    
    # update UserViewSet class to enforce condition like retrieve on the put and delete methods
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split()[1])
            user_from_token = jwt_authenticator.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        if user != user_from_token:
            raise AuthenticationFailed('Token does not match the requested user')

        # Ensure password is hashed if it is being updated
        if 'password' in request.data:
            user.set_password(request.data['password'])
            user.save()
            
            update_session_auth_hash(request, user)
        return Response({"massage": "User updated successfully."}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        jwt_authenticator = JWTAuthentication()
        try:
            validated_token = jwt_authenticator.get_validated_token(request.headers.get('Authorization').split()[1])
            user_from_token = jwt_authenticator.get_user(validated_token)
        except Exception as e:
            raise AuthenticationFailed('Invalid token')

        if user != user_from_token:
            raise AuthenticationFailed('Token does not match the requested user')

        return super().destroy(request, *args, **kwargs)