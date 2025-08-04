import os
import logging
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
# from weasyprint import HTML
from io import BytesIO
import requests
import json

from .models import EmailTemplate, EmailLog, SMSLog, PDFTemplate, PDFLog, SystemSetting

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending emails"""
    
    @staticmethod
    def send_email(template_type, recipient, context=None, user=None, ip_address=None, user_agent=None):
        """Send email using template"""
        try:
            # Get email template
            template = EmailTemplate.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
            
            if not template:
                logger.error(f"Email template not found for type: {template_type}")
                return False
            
            # Prepare context
            if context is None:
                context = {}
            
            # Render email content
            subject = template.subject
            content = template.content
            
            # Replace variables in subject and content
            for key, value in context.items():
                subject = subject.replace(f"{{{{{key}}}}}", str(value))
                content = content.replace(f"{{{{{key}}}}}", str(value))
            
            # Create email log
            email_log = EmailLog.objects.create(
                template=template,
                recipient=recipient,
                subject=subject,
                content=content,
                user=user,
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            # Send email
            try:
                send_mail(
                    subject=subject,
                    message=content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False
                )
                
                # Update log
                email_log.status = 'sent'
                email_log.sent_at = timezone.now()
                email_log.save()
                
                logger.info(f"Email sent successfully to {recipient}")
                return True
                
            except Exception as e:
                # Update log with error
                email_log.status = 'failed'
                email_log.error_message = str(e)
                email_log.save()
                
                logger.error(f"Failed to send email to {recipient}: {str(e)}")
                return False
                
        except Exception as e:
            logger.error(f"Email service error: {str(e)}")
            return False
    
    @staticmethod
    def send_verification_email(email, code, user=None, ip_address=None, user_agent=None):
        """Send verification code email"""
        context = {
            'code': code,
            'email': email,
            'expiry_minutes': 5
        }
        return EmailService.send_email(
            'verification',
            email,
            context,
            user,
            ip_address,
            user_agent
        )
    
    @staticmethod
    def send_welcome_email(email, user, ip_address=None, user_agent=None):
        """Send welcome email"""
        context = {
            'user_name': user.get_full_name() or user.username,
            'email': email,
            'client_code': user.client_code
        }
        return EmailService.send_email(
            'welcome',
            email,
            context,
            user,
            ip_address,
            user_agent
        )
    
    @staticmethod
    def send_password_reset_email(email, reset_url, user=None, ip_address=None, user_agent=None):
        """Send password reset email"""
        context = {
            'reset_url': reset_url,
            'email': email
        }
        return EmailService.send_email(
            'password_reset',
            email,
            context,
            user,
            ip_address,
            user_agent
        )


class SMSService:
    """SMS service for sending SMS"""
    
    @staticmethod
    def send_sms(phone_number, message, user=None, ip_address=None):
        """Send SMS message"""
        try:
            # Create SMS log
            sms_log = SMSLog.objects.create(
                phone_number=phone_number,
                message=message,
                user=user,
                ip_address=ip_address
            )
            
            # Get SMS settings
            sms_api_url = SystemSetting.objects.filter(
                key='sms_api_url',
                is_active=True
            ).first()
            
            sms_api_key = SystemSetting.objects.filter(
                key='sms_api_key',
                is_active=True
            ).first()
            
            if not sms_api_url or not sms_api_key:
                logger.error("SMS API settings not configured")
                sms_log.status = 'failed'
                sms_log.error_message = "SMS API settings not configured"
                sms_log.save()
                return False
            
            # Send SMS (example using external API)
            try:
                # This is a placeholder for actual SMS API integration
                # Replace with your SMS provider's API
                response = requests.post(
                    sms_api_url.value,
                    json={
                        'phone': phone_number,
                        'message': message,
                        'api_key': sms_api_key.value
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    sms_log.status = 'sent'
                    sms_log.sent_at = timezone.now()
                    sms_log.save()
                    
                    logger.info(f"SMS sent successfully to {phone_number}")
                    return True
                else:
                    sms_log.status = 'failed'
                    sms_log.error_message = f"API error: {response.status_code}"
                    sms_log.save()
                    
                    logger.error(f"Failed to send SMS to {phone_number}: API error")
                    return False
                    
            except Exception as e:
                sms_log.status = 'failed'
                sms_log.error_message = str(e)
                sms_log.save()
                
                logger.error(f"Failed to send SMS to {phone_number}: {str(e)}")
                return False
                
        except Exception as e:
            logger.error(f"SMS service error: {str(e)}")
            return False
    
    @staticmethod
    def send_verification_sms(phone_number, code, user=None, ip_address=None):
        """Send verification code SMS"""
        message = f"Tasdiqlash kodingiz: {code}. 5 daqiqa ichida amal qiladi."
        return SMSService.send_sms(phone_number, message, user, ip_address)


class PDFService:
    """PDF service for generating PDF documents"""
    
    @staticmethod
    def generate_pdf(template_type, context=None, user=None, ip_address=None):
        """Generate PDF using template"""
        try:
            # Get PDF template
            template = PDFTemplate.objects.filter(
                template_type=template_type,
                is_active=True
            ).first()
            
            if not template:
                logger.error(f"PDF template not found for type: {template_type}")
                return None
            
            # Prepare context
            if context is None:
                context = {}
            
            # Render HTML content
            html_content = template.html_template
            
            # Replace variables in template
            for key, value in context.items():
                html_content = html_content.replace(f"{{{{{key}}}}}", str(value))
            
            # Add CSS styles
            if template.css_styles:
                html_content = f"""
                <style>
                {template.css_styles}
                </style>
                {html_content}
                """
            
            # Create PDF log
            pdf_log = PDFLog.objects.create(
                template=template,
                user=user,
                ip_address=ip_address
            )
            
            try:
                # Generate PDF using WeasyPrint
                # html = HTML(string=html_content)
                # pdf_bytes = html.write_pdf()
                
                # Update log
                pdf_log.status = 'generated'
                pdf_log.generated_at = timezone.now()
                pdf_log.file_size = 0 # Placeholder, actual size will be calculated later
                pdf_log.save()
                
                logger.info(f"PDF generated successfully for template: {template.name}")
                return None # Return None as PDF generation is commented out
                
            except Exception as e:
                # Update log with error
                pdf_log.status = 'failed'
                pdf_log.error_message = str(e)
                pdf_log.save()
                
                logger.error(f"Failed to generate PDF for template {template.name}: {str(e)}")
                return None
                
        except Exception as e:
            logger.error(f"PDF service error: {str(e)}")
            return None
    
    @staticmethod
    def generate_declaration_pdf(declaration, user=None, ip_address=None):
        """Generate declaration PDF"""
        context = {
            'declaration_number': declaration.declaration_number,
            'declaration_type': declaration.get_declaration_type_display(),
            'product_name': declaration.product_name,
            'product_description': declaration.product_description,
            'product_quantity': declaration.product_quantity,
            'product_value': declaration.product_value,
            'product_currency': declaration.product_currency,
            'contact_name': declaration.contact_name,
            'contact_phone': declaration.contact_phone,
            'contact_email': declaration.contact_email,
            'delivery_address': declaration.delivery_address,
            'created_at': declaration.created_at.strftime('%d.%m.%Y'),
            'status': declaration.get_status_display(),
        }
        
        return PDFService.generate_pdf('declaration', context, user, ip_address)
    
    @staticmethod
    def generate_invoice_pdf(order, user=None, ip_address=None):
        """Generate invoice PDF"""
        context = {
            'order_number': order.order_number,
            'product_name': order.product_name,
            'quantity': order.quantity,
            'unit_price': order.unit_price,
            'total_price': order.total_price,
            'delivery_address': order.delivery_address,
            'order_date': order.order_date.strftime('%d.%m.%Y'),
            'status': order.get_status_display(),
        }
        
        return PDFService.generate_pdf('invoice', context, user, ip_address)


class NotificationService:
    """Notification service for sending various notifications"""
    
    @staticmethod
    def send_order_status_notification(order, user=None, ip_address=None):
        """Send order status notification"""
        if order.user.email:
            context = {
                'order_number': order.order_number,
                'status': order.get_status_display(),
                'product_name': order.product_name,
                'total_price': order.total_price,
                'user_name': order.user.get_full_name() or order.user.username
            }
            
            EmailService.send_email(
                'order_confirmation',
                order.user.email,
                context,
                user,
                ip_address
            )
    
    @staticmethod
    def send_declaration_status_notification(declaration, user=None, ip_address=None):
        """Send declaration status notification"""
        if declaration.user.email:
            context = {
                'declaration_number': declaration.declaration_number,
                'status': declaration.get_status_display(),
                'product_name': declaration.product_name,
                'user_name': declaration.user.get_full_name() or declaration.user.username
            }
            
            EmailService.send_email(
                'declaration_status',
                declaration.user.email,
                context,
                user,
                ip_address
            )
    
    @staticmethod
    def send_support_reply_notification(ticket, message, user=None, ip_address=None):
        """Send support reply notification"""
        if ticket.user.email:
            context = {
                'ticket_number': ticket.ticket_number,
                'subject': ticket.subject,
                'message': message,
                'user_name': ticket.user.get_full_name() or ticket.user.username
            }
            
            EmailService.send_email(
                'support_reply',
                ticket.user.email,
                context,
                user,
                ip_address
            ) 