from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from drf_spectacular.utils import extend_schema  # Import Spectacular Schema
from .serializers import UserSerializer

@extend_schema(
    request=UserSerializer,
    responses={200: UserSerializer},
    description="Register a new user and return a token.",
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=400) 

@extend_schema(
    description="Log in a user and return an authentication token.",
    request=None,
    responses={200: {"token": "string"}},
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username', '').lower()
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"error": "Invalid credentials"}, status=400)

@extend_schema(description="Log out the user by deleting their token.")
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    if hasattr(request.user, 'auth_token'):
        request.user.auth_token.delete()
        return Response({"message": "User logged out"}, status=200)
    return Response({"error": "User is already logged out"}, status=400)

@extend_schema(description="Request a password reset link via email.")
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({"error": 'Email is required'}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=400)

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

@extend_schema(description="Confirm and reset the password using the provided token.")
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({"error": "Invalid user"}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired token"}, status=400)

    new_password = request.data.get('new_password')
    if not new_password:
        return Response({"error": "New password is required"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password has been reset successfully"}, status=200)

@extend_schema(description="Get the authenticated user's profile details.")
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    return Response(data)

@extend_schema(description="Update the authenticated user's profile.")
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)

    return Response(serializer.errors, status=400)
