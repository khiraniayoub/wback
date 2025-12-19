from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
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
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 
            'profile_picture', 'full_name',
            'is_staff', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id','created_at','updated_at','full_name')

class ProfileSerializer(serializers.ModelSerializer):
    full_name=serializers.ReadOnlyField()
    class Meta:
        model=CustomUser
        fields = (
            'id', 'email', 'first_name', 'last_name', 'phone',
            'profile_picture', 'full_name',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'email', 'created_at', 'updated_at', 'full_name')

class ChangePasswordSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True,write_only=True)
    new_password=serializers.CharField(required=True,write_only=True)
    new_password_confirm=serializers.CharField(required=True,write_only=True)

    def validate(self,data):
        if data['new_password']!=data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm":"The passwords do not match."})
        if len(data['new_password'])<8:
            raise serializers.ValidationError({"new_password_confirm":"The password must be at least 8 characters long."})
        return data
    
    def validate_old_password(self,value):
        user=self.context['request'].user
        if  not user.check_password(value):
            raise serializers.ValidationError("The current password is incorrect.")
        return value