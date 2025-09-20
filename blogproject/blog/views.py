from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Post
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User
from .serializers import PostSerializer, UserSerializer
from .permission import IsOwnerOrAdminOrReadOnly


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    role = request.data.get('role', 'user')

    if not username or not password:
        return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Email already taken"}, status=status.HTTP_400_BAD_REQUEST)
    
    if role not in dict(User.ROLE_CHOICES):
        return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

    # Use create_user, which handles password hashing
    user = User.objects.create_user(
        username=username, password=password, email=email, role=role)

    return Response({"message": f"{user} registered successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def post_details(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    permission = IsOwnerOrAdminOrReadOnly()
    self_check = permission.has_object_permission(request, None, post)
    if not self_check:
        return Response({"error": "You do not have permission to edit this post"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        # The user has permission to read
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # The permission class will block this if the user is not the owner or admin.
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # The permission class will block this if the user is not the owner or admin.
        post.delete()
        return Response({"message": "Post deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            # request.user is available because of JWTAuthentication
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
