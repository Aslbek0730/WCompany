from django.db import models
from django.conf import settings
from django.utils import timezone


class SupportTicket(models.Model):
    """Support ticket model for customer support"""
    
    STATUS_CHOICES = [
        ('open', 'Ochiq'),
        ('in_progress', 'Jarayonda'),
        ('waiting_for_customer', 'Mijoz kutilmoqda'),
        ('resolved', 'Hal qilindi'),
        ('closed', 'Yopildi'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Past'),
        ('medium', 'O\'rta'),
        ('high', 'Yuqori'),
        ('urgent', 'Shoshilinch'),
    ]
    
    TICKET_TYPE_CHOICES = [
        ('general', 'Umumiy'),
        ('technical', 'Texnik'),
        ('billing', 'To\'lov'),
        ('order', 'Buyurtma'),
        ('declaration', 'Deklaratsiya'),
        ('other', 'Boshqa'),
    ]
    
    # Basic information
    ticket_number = models.CharField(max_length=20, unique=True, verbose_name="Tiket raqami")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_tickets', verbose_name="Foydalanuvchi")
    
    # Ticket details
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    description = models.TextField(verbose_name="Tavsif")
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPE_CHOICES, default='general', verbose_name="Tiket turi")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name="Ustuvorlik")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Holat")
    
    # Assignment and timestamps
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets',
        verbose_name="Tayinlangan foydalanuvchi"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="Hal qilingan sana")
    closed_at = models.DateTimeField(blank=True, null=True, verbose_name="Yopilgan sana")
    
    # Related objects
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets', verbose_name="Buyurtma")
    declaration = models.ForeignKey('declarations.Declaration', on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets', verbose_name="Deklaratsiya")
    
    # Admin notes
    admin_notes = models.TextField(blank=True, verbose_name="Admin izohlari")
    
    class Meta:
        verbose_name = "Qo'llab-quvvatlash tiketi"
        verbose_name_plural = "Qo'llab-quvvatlash tiketlari"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ticket_number} - {self.subject}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = self.generate_ticket_number()
        
        # Update timestamps based on status
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        elif self.status == 'closed' and not self.closed_at:
            self.closed_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def generate_ticket_number(self):
        """Generate unique ticket number"""
        return f"TKT-{timezone.now().strftime('%Y%m%d')}-{self.id or '0000'}"


class SupportMessage(models.Model):
    """Support message model for ticket communication"""
    
    MESSAGE_TYPE_CHOICES = [
        ('customer', 'Mijoz'),
        ('staff', 'Xodim'),
        ('system', 'Tizim'),
    ]
    
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages', verbose_name="Tiket")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_messages', verbose_name="Yuboruvchi")
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='customer', verbose_name="Xabar turi")
    
    # Message content
    subject = models.CharField(max_length=200, blank=True, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    
    # Attachments
    attachment = models.FileField(upload_to='support_attachments/', blank=True, null=True, verbose_name="Ilova")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    # Read status
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    read_at = models.DateTimeField(blank=True, null=True, verbose_name="O'qilgan sana")
    read_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='read_messages',
        verbose_name="O'qigan foydalanuvchi"
    )
    
    class Meta:
        verbose_name = "Qo'llab-quvvatlash xabari"
        verbose_name_plural = "Qo'llab-quvvatlash xabarlari"
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.ticket.ticket_number} - {self.subject or self.message[:50]}"


class SupportCategory(models.Model):
    """Support category model for organizing tickets"""
    
    name = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Qo'llab-quvvatlash kategoriyasi"
        verbose_name_plural = "Qo'llab-quvvatlash kategoriyalari"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SupportTemplate(models.Model):
    """Support template model for quick responses"""
    
    name = models.CharField(max_length=200, verbose_name="Nomi")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    content = models.TextField(verbose_name="Kontent")
    category = models.ForeignKey(SupportCategory, on_delete=models.CASCADE, related_name='templates', verbose_name="Kategoriya")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Qo'llab-quvvatlash shabloni"
        verbose_name_plural = "Qo'llab-quvvatlash shablonlari"
        ordering = ['name']
    
    def __str__(self):
        return self.name
