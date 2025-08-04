from django.db import models
from django.conf import settings
from django.utils import timezone


class EmailTemplate(models.Model):
    """Email template model for system emails"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('verification', 'Tasdiqlash'),
        ('welcome', 'Xush kelibs'),
        ('password_reset', 'Parolni tiklash'),
        ('order_confirmation', 'Buyurtma tasdiqlash'),
        ('declaration_status', 'Deklaratsiya holati'),
        ('support_reply', 'Qo\'llab-quvvatlash javobi'),
        ('newsletter', 'Yangiliklar'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nomi")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, verbose_name="Shablon turi")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    content = models.TextField(verbose_name="Kontent")
    html_content = models.TextField(blank=True, verbose_name="HTML kontent")
    
    # Variables that can be used in template
    variables = models.JSONField(default=dict, verbose_name="O\'zgaruvchilar")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Email shabloni"
        verbose_name_plural = "Email shablonlari"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class EmailLog(models.Model):
    """Email log model for tracking sent emails"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('sent', 'Yuborildi'),
        ('failed', 'Xatolik'),
        ('bounced', 'Qaytarildi'),
    ]
    
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, related_name='logs', verbose_name="Shablon")
    recipient = models.EmailField(verbose_name="Qabul qiluvchi")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    content = models.TextField(verbose_name="Kontent")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="Yuborilgan sana")
    error_message = models.TextField(blank=True, verbose_name="Xatolik xabari")
    
    # Metadata
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP manzil")
    user_agent = models.TextField(blank=True, verbose_name="Foydalanuvchi agenti")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        verbose_name = "Email log"
        verbose_name_plural = "Email loglari"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient} - {self.subject}"


class SMSLog(models.Model):
    """SMS log model for tracking sent SMS"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('sent', 'Yuborildi'),
        ('failed', 'Xatolik'),
        ('delivered', 'Yetkazildi'),
    ]
    
    phone_number = models.CharField(max_length=20, verbose_name="Telefon raqam")
    message = models.TextField(verbose_name="Xabar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    
    # Tracking
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="Yuborilgan sana")
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name="Yetkazilgan sana")
    error_message = models.TextField(blank=True, verbose_name="Xatolik xabari")
    
    # Metadata
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP manzil")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        verbose_name = "SMS log"
        verbose_name_plural = "SMS loglari"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.phone_number} - {self.message[:50]}"


class SystemSetting(models.Model):
    """System settings model for configuration"""
    
    SETTING_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('pdf', 'PDF'),
        ('general', 'Umumiy'),
        ('security', 'Xavfsizlik'),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    key = models.CharField(max_length=100, unique=True, verbose_name="Kalit")
    value = models.TextField(verbose_name="Qiymat")
    setting_type = models.CharField(max_length=20, choices=SETTING_TYPE_CHOICES, verbose_name="Sozlash turi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Tizim sozlamasi"
        verbose_name_plural = "Tizim sozlamalari"
        ordering = ['setting_type', 'name']
    
    def __str__(self):
        return self.name


class PDFTemplate(models.Model):
    """PDF template model for document generation"""
    
    TEMPLATE_TYPE_CHOICES = [
        ('declaration', 'Deklaratsiya'),
        ('invoice', 'Hisob-faktura'),
        ('receipt', 'Kvitansiya'),
        ('contract', 'Shartnoma'),
        ('report', 'Hisobot'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nomi")
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES, verbose_name="Shablon turi")
    html_template = models.TextField(verbose_name="HTML shablon")
    css_styles = models.TextField(blank=True, verbose_name="CSS stillar")
    
    # Variables that can be used in template
    variables = models.JSONField(default=dict, verbose_name="O\'zgaruvchilar")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "PDF shabloni"
        verbose_name_plural = "PDF shablonlari"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PDFLog(models.Model):
    """PDF log model for tracking generated PDFs"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('generated', 'Yaratildi'),
        ('failed', 'Xatolik'),
    ]
    
    template = models.ForeignKey(PDFTemplate, on_delete=models.CASCADE, related_name='logs', verbose_name="Shablon")
    file_path = models.CharField(max_length=500, blank=True, verbose_name="Fayl yo\'li")
    file_size = models.PositiveIntegerField(blank=True, null=True, verbose_name="Fayl hajmi")
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Holat")
    generated_at = models.DateTimeField(blank=True, null=True, verbose_name="Yaratilgan sana")
    error_message = models.TextField(blank=True, verbose_name="Xatolik xabari")
    
    # Metadata
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Foydalanuvchi")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP manzil")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        verbose_name = "PDF log"
        verbose_name_plural = "PDF loglari"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.template.name} - {self.status}"
