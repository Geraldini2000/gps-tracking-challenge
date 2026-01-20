from rest_framework import serializers
from django.contrib.auth.models import User
from locations.models import UserDevice


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=3)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


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
