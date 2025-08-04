from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User, Passport, UserDocument
from orders.models import Order, OrderStatusUpdate, OrderDocument
from declarations.models import Declaration, DeclarationDocument, DeclarationStatusUpdate
from news.models import News, NewsCategory, Service, CompanyInfo, FAQ
from support.models import SupportTicket, SupportMessage, SupportCategory, SupportTemplate
from utils.models import EmailTemplate, EmailLog, SMSLog, SystemSetting, PDFTemplate, PDFLog


# User Admin
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'client_code', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'gender', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'client_code']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone', 'avatar', 'birth_date', 'gender')}),
        ('Client info', {'fields': ('client_code', 'country', 'city', 'address')}),
        ('Verification', {'fields': ('is_email_verified', 'is_phone_verified', 'email_verification_code', 'phone_verification_code', 'verification_code_expires')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(Passport)
class PassportAdmin(admin.ModelAdmin):
    list_display = ['user', 'series', 'number', 'issue_date', 'expiry_date']
    list_filter = ['issue_date', 'expiry_date']
    search_fields = ['user__email', 'series', 'number']


@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ['user', 'document_type', 'title', 'created_at']
    list_filter = ['document_type', 'created_at']
    search_fields = ['user__email', 'title']


# Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'product_name', 'status', 'delivery_status', 'total_price', 'order_date']
    list_filter = ['status', 'delivery_status', 'order_date']
    search_fields = ['order_number', 'user__email', 'product_name']
    readonly_fields = ['order_number', 'total_price', 'order_date']


@admin.register(OrderStatusUpdate)
class OrderStatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'delivery_status', 'updated_by', 'updated_at']
    list_filter = ['status', 'delivery_status', 'updated_at']
    readonly_fields = ['updated_at']


@admin.register(OrderDocument)
class OrderDocumentAdmin(admin.ModelAdmin):
    list_display = ['order', 'document_type', 'title', 'created_at']
    list_filter = ['document_type', 'created_at']


# Declaration Admin
@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    list_display = ['declaration_number', 'user', 'declaration_type', 'status', 'product_name', 'created_at']
    list_filter = ['declaration_type', 'status', 'created_at']
    search_fields = ['declaration_number', 'user__email', 'product_name']
    readonly_fields = ['declaration_number', 'created_at']


@admin.register(DeclarationStatusUpdate)
class DeclarationStatusUpdateAdmin(admin.ModelAdmin):
    list_display = ['declaration', 'status', 'updated_by', 'updated_at']
    list_filter = ['status', 'updated_at']
    readonly_fields = ['updated_at']


@admin.register(DeclarationDocument)
class DeclarationDocumentAdmin(admin.ModelAdmin):
    list_display = ['declaration', 'document_type', 'title', 'created_at']
    list_filter = ['document_type', 'created_at']


# News Admin
@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'author', 'published_at']
    list_filter = ['status', 'category', 'published_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'price', 'currency', 'is_active', 'order']
    list_filter = ['service_type', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'info_type', 'is_active', 'order']
    list_filter = ['info_type', 'is_active']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'order']
    list_filter = ['is_active']


# Support Admin
@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'user', 'subject', 'ticket_type', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'ticket_type', 'created_at']
    search_fields = ['ticket_number', 'user__email', 'subject']
    readonly_fields = ['ticket_number', 'created_at']


@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'message_type', 'created_at']
    list_filter = ['message_type', 'created_at']
    search_fields = ['ticket__ticket_number', 'sender__email']


@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']


@admin.register(SupportTemplate)
class SupportTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    list_filter = ['category', 'is_active']


# Utils Admin
@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active']
    list_filter = ['template_type', 'is_active']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'subject', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'sent_at', 'created_at']
    readonly_fields = ['created_at']


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'status', 'sent_at', 'created_at']
    list_filter = ['status', 'sent_at', 'created_at']
    readonly_fields = ['created_at']


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'setting_type', 'is_active']
    list_filter = ['setting_type', 'is_active']
    search_fields = ['name', 'key']


@admin.register(PDFTemplate)
class PDFTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active']
    list_filter = ['template_type', 'is_active']


@admin.register(PDFLog)
class PDFLogAdmin(admin.ModelAdmin):
    list_display = ['template', 'status', 'file_size', 'generated_at', 'created_at']
    list_filter = ['status', 'generated_at', 'created_at']
    readonly_fields = ['created_at']


# Admin site customization
admin.site.site_header = "WWW Backend Administration"
admin.site.site_title = "WWW Backend Admin"
admin.site.index_title = "Welcome to WWW Backend Administration" 