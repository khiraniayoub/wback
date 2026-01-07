from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer,ProfileSerializer,ChangePasswordSerializer
from .models import User
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action


class RegistrationView(APIView):
    @extend_schema(
        summary="user registration",
        description="Creates a new user account in the platform.",
        request=RegistrationSerializer,
        responses={201: RegistrationSerializer,400: None}
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User successfully registered."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    @extend_schema(
        summary="User login",
        description="Authenticates credentials and returns the JWT access and refresh tokens.",
        request=LoginSerializer,
        responses={200: {"type": "object", "properties": {
            "refresh": {"type": "string"},
            "access": {"type": "string"}
        }}}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, status=status.HTTP_200_OK)
@extend_schema_view(
    list=extend_schema(summary="List all users", description="Retrieve a list of all registered users."),
    retrieve=extend_schema(summary="Get user details", description="Retrieve detailed information about a specific user by ID."),
    #create=extend_schema(summary="Create user (Admin Only)", description="Manually create a user. Restricted to staff/admins."),
    update=extend_schema(summary="Update user", description="Full update of a user's information."),
    partial_update=extend_schema(summary="Patch user", description="Partial update of a user's information."),
    destroy=extend_schema(summary="Delete user", description="Permanently remove a user from the database.")
)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users.
    Requires Admin privileges to access.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get','patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer=ProfileSerializer(
            request.user,
            data=request.data if request.method== 'PATCH' else None,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""class ProfileView(APIView):
    permission_classes=[IsAuthenticated]

    @extend_schema(
        summary="View my profile", 
        description="Get the profile details of the currently authenticated user.",
        responses={200: ProfileSerializer}
    )
    def get(self, request):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(
        summary="Update my profile", 
        description="Update information for the currently authenticated user.",
        request=ProfileSerializer, 
        responses={200: ProfileSerializer}
    )
    def put(self,request):
        serializer=ProfileSerializer(request.user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(exclude=True) 
    def patch(self, request):
        return self.put(request)"""
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Change password",
        description="Updates the user password and returns new JWT access and refresh tokens.",
        request=ChangePasswordSerializer,
        responses={
            200: {
                "type": "object", 
                "properties": {
                    "message": {"type": "string"}, 
                    "refresh": {"type": "string"},
                    "access": {"type": "string"}
                }
            }
        }
    )
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

            # Generar nuevos tokens JWT
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Password successfully updated.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
