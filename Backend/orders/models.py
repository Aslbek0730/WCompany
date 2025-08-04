from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Order(models.Model):
    """Order model for client orders"""
    
    ORDER_STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('processing', 'Jarayonda'),
        ('shipped', 'Yuborildi'),
        ('delivered', 'Yetkazildi'),
        ('cancelled', 'Bekor qilindi'),
        ('returned', 'Qaytarildi'),
    ]
    
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('in_transit', 'Yo\'lda'),
        ('out_for_delivery', 'Yetkazish uchun chiqdi'),
        ('delivered', 'Yetkazildi'),
        ('failed', 'Muvaffaqiyatsiz'),
    ]
    
    # Basic order information
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Buyurtma raqami")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name="Foydalanuvchi")
    
    # Product information
    product_name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    product_description = models.TextField(blank=True, verbose_name="Mahsulot tavsifi")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdori")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Birlik narxi")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Umumiy narx")
    
    # Order status
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending', verbose_name="Holat")
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending', verbose_name="Yetkazish holati")
    
    # Tracking information
    tracking_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Izlash raqami")
    tracking_url = models.URLField(blank=True, null=True, verbose_name="Izlash havolasi")
    
    # Delivery information
    delivery_address = models.TextField(verbose_name="Yetkazish manzili")
    delivery_phone = models.CharField(max_length=20, verbose_name="Yetkazish telefon raqami")
    delivery_notes = models.TextField(blank=True, verbose_name="Yetkazish izohlari")
    
    # Timestamps
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Buyurtma sanasi")
    estimated_delivery = models.DateTimeField(blank=True, null=True, verbose_name="Taxminiy yetkazish sanasi")
    actual_delivery = models.DateTimeField(blank=True, null=True, verbose_name="Haqiqiy yetkazish sanasi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    # Admin notes
    admin_notes = models.TextField(blank=True, verbose_name="Admin izohlari")
    
    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-order_date']
    
    def __str__(self):
        return f"{self.order_number} - {self.product_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        if not self.total_price:
            self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        return f"ORD-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


class OrderStatusUpdate(models.Model):
    """Order status update history"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_updates', verbose_name="Buyurtma")
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES, verbose_name="Holat")
    delivery_status = models.CharField(max_length=20, choices=Order.DELIVERY_STATUS_CHOICES, verbose_name="Yetkazish holati")
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Yangilagan foydalanuvchi")
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Buyurtma holati yangilanishi"
        verbose_name_plural = "Buyurtma holati yangilanishlari"
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.status}"


class OrderDocument(models.Model):
    """Order related documents"""
    
    DOCUMENT_TYPES = [
        ('invoice', 'Hisob-faktura'),
        ('receipt', 'Kvitansiya'),
        ('tracking', 'Izlash hujjati'),
        ('other', 'Boshqa'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='documents', verbose_name="Buyurtma")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Hujjat turi")
    title = models.CharField(max_length=200, verbose_name="Nomi")
    file = models.FileField(upload_to='order_documents/', verbose_name="Fayl")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    
    class Meta:
        verbose_name = "Buyurtma hujjati"
        verbose_name_plural = "Buyurtma hujjatlari"
    
    def __str__(self):
        return f"{self.order.order_number} - {self.title}"
