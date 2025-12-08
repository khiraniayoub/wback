from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import LoginSerializer
from rest_framework.decorators import api_view


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)

class PingView(APIView):
    def get(self, request):
        return Response({"message": "pong"})
    

    
@api_view(['POST'])
def login(request):
    email = request.datos.get('email')
    password = request.datos.get('password')

    return Response({
        "status": "ok",
        "email": email,
        "password": password
    })