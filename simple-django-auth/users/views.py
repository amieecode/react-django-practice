from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from .serializers import UserSerializer

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=400) 


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error": "Invalid credentials"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Logs out the user by deleting their authentication token"""
    token = request.user.auth_token
    if token:
        token.delete()
    return Response({"message": "User logged out"}, status=200)


@api_view(['POST'])
def password_reset_request(request):
    """send Password reset email"""
    email = request.data.get('email')
    if not email:
        return Response({"error": 'Email is required'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User does not exit"}, status=400)
    
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = request.build_absolute_uri(reverse("password_reset_confirm", args=[uid, token]))

    send_mail(
        "Password reset request",
        f"Click the link to reset your password:\n{reset_link}",
        "your_email@gmail.com",
        [email],
        fail_silently=False,
    )
    return Response({"message": "Password reset email sent"}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """Get logged in user's profile"""
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """"Update logged in user's profile"""
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)