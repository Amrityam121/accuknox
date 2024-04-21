# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name','last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("get_user_model is              ",validated_data)
        user = get_user_model().objects.create_user(**validated_data)
        return user
