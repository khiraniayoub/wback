from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import User

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 
            'profile_picture', 'full_name',
            'is_staff', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id','created_at','updated_at','full_name')

class ProfileSerializer(serializers.ModelSerializer):
    full_name=serializers.ReadOnlyField()
    class Meta:
        model=User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone',
            'profile_picture', 'full_name',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'email', 'created_at', 'updated_at', 'full_name')

class ChangePasswordSerializer(serializers.Serializer):
    current_password=serializers.CharField(required=True,write_only=True)
    new_password=serializers.CharField(required=True,write_only=True)
    new_password_confirm=serializers.CharField(required=True,write_only=True)

    def validate(self,data):
        if data['new_password']!=data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm":"The passwords do not match."})

        try:
            validate_password(data['new_password'], user=self.context['request'].user)
        except DjangoValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return data

    def validate_current_password(self,value):
        user=self.context['request'].user
        if  not user.check_password(value):
            raise serializers.ValidationError("The current password is incorrect.")
        return value
