from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid
import random
import string


def generate_client_code():
    """Generate unique client code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class User(AbstractUser):
    """Custom User model with extended fields"""
    
    # Basic fields
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqam")
    
    # Profile fields
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil rasmi")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Tug'ilgan sana")
    gender = models.CharField(
        max_length=10,
        choices=[
            ('male', 'Erkak'),
            ('female', 'Ayol'),
        ],
        blank=True,
        verbose_name="Jinsi"
    )
    
    # Client specific fields
    client_code = models.CharField(
        max_length=10,
        unique=True,
        default=generate_client_code,
        verbose_name="Mijoz kodi"
    )
    
    # Verification fields
    is_email_verified = models.BooleanField(default=False, verbose_name="Email tasdiqlangan")
    is_phone_verified = models.BooleanField(default=False, verbose_name="Telefon tasdiqlangan")
    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    phone_verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expires = models.DateTimeField(blank=True, null=True)
    
    # Location fields
    country = models.CharField(max_length=100, blank=True, verbose_name="Davlat")
    city = models.CharField(max_length=100, blank=True, verbose_name="Shahar")
    address = models.TextField(blank=True, verbose_name="Manzil")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    # Override username field
    username = models.CharField(max_length=150, unique=True, verbose_name="Foydalanuvchi nomi")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
    
    def __str__(self):
        return f"{self.email} ({self.client_code})"
    
    def save(self, *args, **kwargs):
        if not self.client_code:
            self.client_code = generate_client_code()
        super().save(*args, **kwargs)


class Passport(models.Model):
    """Passport information model"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='passport', verbose_name="Foydalanuvchi")
    series = models.CharField(max_length=2, verbose_name="Seriya")
    number = models.CharField(max_length=7, verbose_name="Raqam")
    issue_date = models.DateField(verbose_name="Berilgan sana")
    expiry_date = models.DateField(verbose_name="Amal qilish muddati")
    issuing_authority = models.CharField(max_length=200, verbose_name="Bergan organ")
    passport_photo = models.ImageField(upload_to='passports/', blank=True, null=True, verbose_name="Pasport rasmi")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Pasport"
        verbose_name_plural = "Pasportlar"
    
    def __str__(self):
        return f"{self.user.email} - {self.series}{self.number}"
    
    @property
    def full_number(self):
        return f"{self.series}{self.number}"


class UserDocument(models.Model):
    """User documents model"""
    
    DOCUMENT_TYPES = [
        ('passport', 'Pasport'),
        ('id_card', 'ID karta'),
        ('driving_license', 'Haydovchilik guvohnomasi'),
        ('other', 'Boshqa'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents', verbose_name="Foydalanuvchi")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    title = models.CharField(max_length=200, verbose_name="Nomi")
    file = models.FileField(upload_to='documents/', verbose_name="Fayl")
    description = models.TextField(blank=True, verbose_name="Izoh")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        verbose_name = "Foydalanuvchi hujjati"
        verbose_name_plural = "Foydalanuvchi hujjatlari"
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"
