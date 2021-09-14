import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from django.contrib.auth.models import User
from account.serializers.user_serializer import UserSerializer
from account.controllers.user_controller import (
    register_new_user,
    retrieve_all_users,
    retrieve_user_by_id
)
from drf_yasg.utils import swagger_auto_schema


class UserView(APIView):
    logger = logging.getLogger(__name__)

    @swagger_auto_schema(
        operation_description='Retrieve user(s) registered in Search Videos.',
        responses={200: UserSerializer})
    def get(self, request, id=None):
        try:
            if id is None:
                users = retrieve_all_users()
                users = [UserSerializer(user).data for user in users]
                return Response(users, status=status.HTTP_200_OK)
            user_instance = retrieve_user_by_id(id)
            user = UserSerializer(user_instance).data
            return Response(user, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            self.logger.exception(f'User {id} does not exist.')
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            self.logger.exception('Unable to retrieve user(s).')
            return Response(
                {'detail': 'Unable to retrieve user(s). Please try again later.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @swagger_auto_schema(
        operation_description='Register a user in Search Videos.',
        responses={201: UserSerializer})
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_instance = register_new_user(serializer.validated_data)
            user = UserSerializer(user_instance).data
            return Response(user, status=status.HTTP_201_CREATED)
        except ValidationError:
            self.logger.exception('Invalid fields found while registering new user.')
            return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            self.logger.exception('Failed to register new user.')
            return Response({
                'detail': 'Somenthing went wrong during user registration. Please try again later.'},
                status=status.HTTP_400_BAD_REQUEST
            )
