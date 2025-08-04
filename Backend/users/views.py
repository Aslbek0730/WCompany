from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import User, Passport, UserDocument
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserProfileUpdateSerializer, PassportSerializer, UserDocumentSerializer,
    VerificationCodeSerializer, SendVerificationCodeSerializer, ChangePasswordSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """User registration view"""
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate verification code
        verification_code = ''.join(random.choices(string.digits, k=6))
        user.email_verification_code = verification_code
        user.verification_code_expires = timezone.now() + timedelta(minutes=5)
        user.save()
        
        # TODO: Send verification code via email
        # send_verification_email(user.email, verification_code)
        
        return Response({
            'message': 'Foydalanuvchi muvaffaqiyatli ro\'yxatdan o\'tdi. Tasdiqlash kodi yuborildi.',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """User login view"""
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': UserProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile view"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    """User profile update view"""
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PassportView(generics.RetrieveUpdateAPIView):
    """Passport information view"""
    serializer_class = PassportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return Passport.objects.get_or_create(user=self.request.user)[0]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserDocumentView(generics.ListCreateAPIView):
    """User documents view"""
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserDocumentDetailView(generics.RetrieveDestroyAPIView):
    """User document detail view"""
    serializer_class = UserDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_verification_code(request):
    """Send verification code to email or phone"""
    serializer = SendVerificationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data.get('email')
    phone = serializer.validated_data.get('phone')
    
    try:
        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate verification code
    verification_code = ''.join(random.choices(string.digits, k=6))
    
    if email:
        user.email_verification_code = verification_code
    else:
        user.phone_verification_code = verification_code
    
    user.verification_code_expires = timezone.now() + timedelta(minutes=5)
    user.save()
    
    # TODO: Send verification code via email or SMS
    # if email:
    #     send_verification_email(email, verification_code)
    # else:
    #     send_verification_sms(phone, verification_code)
    
    return Response({
        'message': 'Tasdiqlash kodi yuborildi'
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_code(request):
    """Verify email or phone verification code"""
    serializer = VerificationCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    email = serializer.validated_data.get('email')
    phone = serializer.validated_data.get('phone')
    code = serializer.validated_data['code']
    
    try:
        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({'error': 'Foydalanuvchi topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    # Check if code is expired
    if user.verification_code_expires and user.verification_code_expires < timezone.now():
        return Response({'error': 'Tasdiqlash kodi muddati tugagan'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Verify code
    if email and user.email_verification_code == code:
        user.is_email_verified = True
        user.email_verification_code = None
        user.verification_code_expires = None
        user.save()
        return Response({'message': 'Email muvaffaqiyatli tasdiqlandi'}, status=status.HTTP_200_OK)
    elif phone and user.phone_verification_code == code:
        user.is_phone_verified = True
        user.phone_verification_code = None
        user.verification_code_expires = None
        user.save()
        return Response({'message': 'Telefon raqam muvaffaqiyatli tasdiqlandi'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Noto\'g\'ri tasdiqlash kodi'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    """Change user password"""
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    
    return Response({'message': 'Parol muvaffaqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """User logout"""
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Muvaffaqiyatli chiqildi'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Noto\'g\'ri token'}, status=status.HTTP_400_BAD_REQUEST)
