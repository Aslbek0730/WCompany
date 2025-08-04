from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Declaration(models.Model):
    """Declaration model for customs declarations"""
    
    DECLARATION_STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('submitted', 'Yuborildi'),
        ('under_review', 'Ko\'rib chiqilmoqda'),
        ('approved', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
        ('completed', 'Bajarildi'),
    ]
    
    DECLARATION_TYPE_CHOICES = [
        ('import', 'Import'),
        ('export', 'Eksport'),
        ('transit', 'Tranzit'),
    ]
    
    # Basic declaration information
    declaration_number = models.CharField(max_length=20, unique=True, verbose_name="Deklaratsiya raqami")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='declarations', verbose_name="Foydalanuvchi")
    
    # Declaration details
    declaration_type = models.CharField(max_length=20, choices=DECLARATION_TYPE_CHOICES, verbose_name="Deklaratsiya turi")
    status = models.CharField(max_length=20, choices=DECLARATION_STATUS_CHOICES, default='draft', verbose_name="Holat")
    
    # Order information
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='declarations', verbose_name="Buyurtma")
    
    # Passport information
    passport_series = models.CharField(max_length=2, verbose_name="Pasport seriyasi")
    passport_number = models.CharField(max_length=7, verbose_name="Pasport raqami")
    passport_issue_date = models.DateField(verbose_name="Pasport berilgan sana")
    passport_expiry_date = models.DateField(verbose_name="Pasport amal qilish muddati")
    passport_issuing_authority = models.CharField(max_length=200, verbose_name="Pasport bergan organ")
    
    # Contact information
    contact_name = models.CharField(max_length=200, verbose_name="Aloqa qiluvchi shaxs")
    contact_phone = models.CharField(max_length=20, verbose_name="Aloqa telefon raqami")
    contact_email = models.EmailField(verbose_name="Aloqa email")
    
    # Delivery information
    delivery_address = models.TextField(verbose_name="Yetkazish manzili")
    delivery_country = models.CharField(max_length=100, verbose_name="Yetkazish davlati")
    delivery_city = models.CharField(max_length=100, verbose_name="Yetkazish shahri")
    
    # Product information
    product_name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    product_description = models.TextField(verbose_name="Mahsulot tavsifi")
    product_quantity = models.PositiveIntegerField(verbose_name="Mahsulot miqdori")
    product_unit = models.CharField(max_length=50, verbose_name="O\'lchov birligi")
    product_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Mahsulot qiymati")
    product_currency = models.CharField(max_length=3, default='USD', verbose_name="Valyuta")
    
    # Customs information
    customs_code = models.CharField(max_length=20, blank=True, verbose_name="Bojxona kodi")
    customs_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Bojxona qiymati")
    customs_duty = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Bojxona to\'lovi")
    
    # Additional information
    notes = models.TextField(blank=True, verbose_name="Qo\'shimcha ma\'lumotlar")
    admin_notes = models.TextField(blank=True, verbose_name="Admin izohlari")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    submitted_at = models.DateTimeField(blank=True, null=True, verbose_name="Yuborilgan sana")
    reviewed_at = models.DateTimeField(blank=True, null=True, verbose_name="Ko\'rib chiqilgan sana")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="Bajarilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    # Review information
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='reviewed_declarations',
        verbose_name="Ko\'rib chiqgan foydalanuvchi"
    )
    rejection_reason = models.TextField(blank=True, verbose_name="Rad etish sababi")
    
    class Meta:
        verbose_name = "Deklaratsiya"
        verbose_name_plural = "Deklaratsiyalar"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.declaration_number} - {self.product_name}"
    
    def save(self, *args, **kwargs):
        if not self.declaration_number:
            self.declaration_number = self.generate_declaration_number()
        super().save(*args, **kwargs)
    
    def generate_declaration_number(self):
        """Generate unique declaration number"""
        return f"DEC-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


class DeclarationDocument(models.Model):
    """Declaration related documents"""
    
    DOCUMENT_TYPES = [
        ('invoice', 'Hisob-faktura'),
        ('packing_list', 'O\'rash ro\'yxati'),
        ('certificate', 'Sertifikat'),
        ('permit', 'Ruxsatnoma'),
        ('other', 'Boshqa'),
    ]
    
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name='documents', verbose_name="Deklaratsiya")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    title = models.CharField(max_length=200, verbose_name="Nomi")
    file = models.FileField(upload_to='declaration_documents/', verbose_name="Fayl")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        verbose_name = "Deklaratsiya hujjati"
        verbose_name_plural = "Deklaratsiya hujjatlari"
    
    def __str__(self):
        return f"{self.declaration.declaration_number} - {self.title}"


class DeclarationStatusUpdate(models.Model):
    """Declaration status update history"""
    
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, related_name='status_updates', verbose_name="Deklaratsiya")
    status = models.CharField(max_length=20, choices=Declaration.DECLARATION_STATUS_CHOICES, verbose_name="Holat")
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Yangilagan foydalanuvchi")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Deklaratsiya holati yangilanishi"
        verbose_name_plural = "Deklaratsiya holati yangilanishlari"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.declaration.declaration_number} - {self.status}"
