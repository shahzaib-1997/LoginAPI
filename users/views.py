from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer, PasswordChangeSerializer, CustomTokenSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated



class RegistrationView(APIView):

    renderer_classes =[UserRenderers]    
    def post(self, request):
    
        szr = RegistrationSerializer(data=request.data)
        szr.is_valid(raise_exception=True)
        user = szr.save()
        token = CustomTokenSerializer.get_token(user=user)

        return Response({'msg': 'Registration success.', 'token': {
                                'refresh': str(token),
                                'access': str(token.access_token),
                             }},
            status= status.HTTP_201_CREATED
        )


class LoginView(APIView):

    renderer_classes = [UserRenderers]
    def post(self, request):

        szr = LoginSerializer(data=request.data)
        szr.is_valid(raise_exception=True)
        email = szr.data.get('email')
        password = szr.data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            token = CustomTokenSerializer.get_token(user=user)
            return Response({'msg': 'Login success.', 'token': {
                                'refresh': str(token),
                                'access': str(token.access_token),
                             }
                            },
                status= status.HTTP_200_OK
            )
        
        return Response({'errors': {'non_field_errors': ['Email or password is not valid!!!']}},
            status=status.HTTP_404_NOT_FOUND
        )

      
class ProfileView(APIView):

    renderer_classes = [UserRenderers]    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        szr = ProfileSerializer(request.user)
        return Response(szr.data, status=status.HTTP_200_OK)



class PasswordChangeView(APIView):

    renderer_classes = [UserRenderers]    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        szr = PasswordChangeSerializer(data=request.data, context= {'user': request.user})
        szr.is_valid(raise_exception=True)
        return Response({'msg': 'Password changed successfully.'},
            status= status.HTTP_200_OK
        )
