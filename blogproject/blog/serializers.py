from rest_framework import serializers
from .models import Post, User


class PostSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_role = serializers.ReadOnlyField(source='owner.role')
    class Meta:
        model = Post
        fields = ['id', 'title', 'owner_role',
                  'owner_username', 'content', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'country', 'first_name', 'last_name']
