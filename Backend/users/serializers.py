from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, Passport, UserDocument


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'birth_date', 'gender',
            'country', 'city', 'address'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Parollar mos kelmadi")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError('Noto\'g\'ri email yoki parol')
            if not user.is_active:
                raise serializers.ValidationError('Foydalanuvchi faol emas')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Email va parol talab qilinadi')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'phone', 'avatar', 'birth_date', 'gender', 'client_code',
            'is_email_verified', 'is_phone_verified', 'country', 'city',
            'address', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'client_code', 'created_at', 'updated_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone', 'avatar', 'birth_date',
            'gender', 'country', 'city', 'address'
        ]


class PassportSerializer(serializers.ModelSerializer):
    """Serializer for passport information"""
    
    class Meta:
        model = Passport
        fields = [
            'id', 'series', 'number', 'issue_date', 'expiry_date',
            'issuing_authority', 'passport_photo', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        # Validate passport number format (Uzbekistan format)
        series = attrs.get('series', '')
        number = attrs.get('number', '')
        
        if len(series) != 2:
            raise serializers.ValidationError("Seriya 2 ta harf bo'lishi kerak")
        
        if len(number) != 7:
            raise serializers.ValidationError("Raqam 7 ta raqam bo'lishi kerak")
        
        if not number.isdigit():
            raise serializers.ValidationError("Raqam faqat raqamlardan iborat bo'lishi kerak")
        
        return attrs


class UserDocumentSerializer(serializers.ModelSerializer):
    """Serializer for user documents"""
    
    class Meta:
        model = UserDocument
        fields = [
            'id', 'document_type', 'title', 'file', 'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class VerificationCodeSerializer(serializers.Serializer):
    """Serializer for verification code"""
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    code = serializers.CharField(max_length=6)
    
    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        
        if not email and not phone:
            raise serializers.ValidationError("Email yoki telefon raqam talab qilinadi")
        
        return attrs


class SendVerificationCodeSerializer(serializers.Serializer):
    """Serializer for sending verification code"""
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    
    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone')
        
        if not email and not phone:
            raise serializers.ValidationError("Email yoki telefon raqam talab qilinadi")
        
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Yangi parollar mos kelmadi")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Hozirgi parol noto'g'ri")
        return value 