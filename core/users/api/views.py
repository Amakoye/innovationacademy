from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .serializers import ParentSignupSerializer, AdminSignupSerializer, UserSerializer
from .permissions import isAdminUser, isParentUser


class ParentSignupView(generics.GenericAPIView):
    serializer_class = ParentSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })


class AdminSignupView(generics.GenericAPIView):
    serializer_class = AdminSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.get(user=user).key,
            "message": "account created successfully"
        })


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'is_admin': user.is_admin
        })


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class AdminOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & isAdminUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ParentOnlyView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated & isParentUser]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
