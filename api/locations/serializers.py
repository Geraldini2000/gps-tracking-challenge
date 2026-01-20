from rest_framework import serializers
from django.contrib.auth.models import User
from locations.models import UserDevice


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class DeviceRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ('device_id', 'device_name')

    def validate_device_id(self, value):
        if UserDevice.objects.filter(device_id=value).exists():
            raise serializers.ValidationError("This device is already registered to another user")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class UserDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDevice
        fields = ('id', 'device_id', 'device_name', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
