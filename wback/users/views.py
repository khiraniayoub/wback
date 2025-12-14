from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer,ProfileSerializer,ChangePasswordSerializer
from .models import CustomUser


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario registrado exitosamente."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios.
    Requiere autenticación para acceder.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data)
    def put(self,request):
        serializer=ProfileSerializer(request.user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            # Cambiar la contraseña
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Actualizar el token
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            
            return Response({
                "message": "Contraseña actualizada exitosamente.",
                "token": new_token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)