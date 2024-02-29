from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length = 20)

    def create(self, validated_data):
        return User.objects.create(username = validated_data.get('phone'), phone=validated_data.get('phone'))