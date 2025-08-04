from django.db import models
from django.conf import settings
from django.utils import timezone


class NewsCategory(models.Model):
    """News category model"""
    
    name = models.CharField(max_length=100, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Yangilik kategoriyasi"
        verbose_name_plural = "Yangilik kategoriyalari"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class News(models.Model):
    """News model for company updates"""
    
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('published', 'Nashr etilgan'),
        ('archived', 'Arxivlangan'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Kontent")
    excerpt = models.TextField(blank=True, verbose_name="Qisqacha tavsif")
    
    # Media
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Rasm")
    
    # Category and status
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news', verbose_name="Kategoriya")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Holat")
    
    # Author and timestamps
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news', verbose_name="Muallif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="Nashr etilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta sarlavha")
    meta_description = models.TextField(blank=True, verbose_name="Meta tavsif")
    
    class Meta:
        verbose_name = "Yangilik"
        verbose_name_plural = "Yangiliklar"
        ordering = ['-published_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class Service(models.Model):
    """Service model for company services"""
    
    SERVICE_TYPE_CHOICES = [
        ('import', 'Import xizmati'),
        ('export', 'Eksport xizmati'),
        ('customs', 'Bojxona xizmati'),
        ('logistics', 'Logistika xizmati'),
        ('consulting', 'Maslahat xizmati'),
        ('other', 'Boshqa'),
    ]
    
    # Basic information
    name = models.CharField(max_length=200, verbose_name="Xizmat nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Tavsif")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Qisqacha tavsif")
    
    # Service details
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, verbose_name="Xizmat turi")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Narx")
    currency = models.CharField(max_length=3, default='USD', verbose_name="Valyuta")
    
    # Media
    icon = models.ImageField(upload_to='services/icons/', blank=True, null=True, verbose_name="Ikonka")
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name="Rasm")
    
    # Status and ordering
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Xizmat"
        verbose_name_plural = "Xizmatlar"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class CompanyInfo(models.Model):
    """Company information model"""
    
    INFO_TYPE_CHOICES = [
        ('about', 'Kompaniya haqida'),
        ('delivery', 'Yetkazish'),
        ('pricing', 'Narxlar'),
        ('faq', 'Ko\'p so\'raladigan savollar'),
        ('contact', 'Aloqa ma\'lumotlari'),
        ('terms', 'Foydalanish shartlari'),
        ('privacy', 'Maxfiylik siyosati'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    info_type = models.CharField(max_length=20, choices=INFO_TYPE_CHOICES, verbose_name="Ma'lumot turi")
    content = models.TextField(verbose_name="Kontent")
    
    # Status and ordering
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Kompaniya ma'lumoti"
        verbose_name_plural = "Kompaniya ma'lumotlari"
        ordering = ['order', 'title']
        unique_together = ['info_type', 'is_active']
    
    def __str__(self):
        return f"{self.get_info_type_display()} - {self.title}"


class FAQ(models.Model):
    """FAQ model for frequently asked questions"""
    
    question = models.CharField(max_length=500, verbose_name="Savol")
    answer = models.TextField(verbose_name="Javob")
    
    # Status and ordering
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")
    
    class Meta:
        verbose_name = "Ko'p so'raladigan savol"
        verbose_name_plural = "Ko'p so'raladigan savollar"
        ordering = ['order', 'question']
    
    def __str__(self):
        return self.question
