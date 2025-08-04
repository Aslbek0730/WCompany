from rest_framework import serializers
from .models import SupportTicket, SupportMessage, SupportCategory, SupportTemplate


class SupportTicketSerializer(serializers.ModelSerializer):
    """Serializer for support ticket model"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'ticket_number', 'user', 'user_name', 'subject', 'description',
            'ticket_type', 'priority', 'status', 'assigned_to', 'assigned_to_name',
            'order', 'declaration', 'admin_notes', 'created_at', 'updated_at',
            'resolved_at', 'closed_at'
        ]
        read_only_fields = ['id', 'ticket_number', 'user_name', 'assigned_to_name', 'created_at', 'updated_at', 'resolved_at', 'closed_at']


class SupportTicketCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating support tickets"""
    
    class Meta:
        model = SupportTicket
        fields = [
            'subject', 'description', 'ticket_type', 'priority',
            'order', 'declaration'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SupportTicketUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating support tickets (admin only)"""
    
    class Meta:
        model = SupportTicket
        fields = [
            'status', 'priority', 'assigned_to', 'admin_notes'
        ]


class SupportTicketListSerializer(serializers.ModelSerializer):
    """Serializer for support ticket list view"""
    
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    latest_message = serializers.SerializerMethodField()
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'ticket_number', 'subject', 'ticket_type', 'priority',
            'status', 'user_name', 'assigned_to_name', 'created_at',
            'updated_at', 'latest_message'
        ]
        read_only_fields = ['id', 'ticket_number', 'user_name', 'assigned_to_name', 'created_at', 'updated_at']
    
    def get_latest_message(self, obj):
        latest_message = obj.messages.last()
        if latest_message:
            return {
                'message': latest_message.message[:100] + '...' if len(latest_message.message) > 100 else latest_message.message,
                'created_at': latest_message.created_at
            }
        return None


class SupportMessageSerializer(serializers.ModelSerializer):
    """Serializer for support message model"""
    
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    
    class Meta:
        model = SupportMessage
        fields = [
            'id', 'ticket', 'sender', 'sender_name', 'message_type',
            'subject', 'message', 'attachment', 'created_at', 'updated_at',
            'is_read', 'read_at'
        ]
        read_only_fields = ['id', 'sender_name', 'created_at', 'updated_at']


class SupportMessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating support messages"""
    
    class Meta:
        model = SupportMessage
        fields = [
            'ticket', 'subject', 'message', 'attachment'
        ]
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        
        # Set message type based on user
        if self.context['request'].user.is_staff:
            validated_data['message_type'] = 'staff'
        else:
            validated_data['message_type'] = 'customer'
        
        return super().create(validated_data)


class SupportMessageUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating support messages"""
    
    class Meta:
        model = SupportMessage
        fields = [
            'subject', 'message', 'attachment'
        ]


class SupportCategorySerializer(serializers.ModelSerializer):
    """Serializer for support category model"""
    
    class Meta:
        model = SupportCategory
        fields = [
            'id', 'name', 'description', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SupportCategoryCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating support categories"""
    
    class Meta:
        model = SupportCategory
        fields = [
            'name', 'description', 'is_active'
        ]


class SupportTemplateSerializer(serializers.ModelSerializer):
    """Serializer for support template model"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = SupportTemplate
        fields = [
            'id', 'name', 'subject', 'content', 'category', 'category_name',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'category_name', 'created_at', 'updated_at']


class SupportTemplateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating support templates"""
    
    class Meta:
        model = SupportTemplate
        fields = [
            'name', 'subject', 'content', 'category', 'is_active'
        ]


class SupportTicketDetailSerializer(serializers.ModelSerializer):
    """Detailed support ticket serializer with messages"""
    
    messages = SupportMessageSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    
    class Meta:
        model = SupportTicket
        fields = [
            'id', 'ticket_number', 'user', 'user_name', 'subject', 'description',
            'ticket_type', 'priority', 'status', 'assigned_to', 'assigned_to_name',
            'order', 'declaration', 'admin_notes', 'created_at', 'updated_at',
            'resolved_at', 'closed_at', 'messages'
        ]
        read_only_fields = ['id', 'ticket_number', 'user_name', 'assigned_to_name', 'created_at', 'updated_at', 'resolved_at', 'closed_at']


class SupportStatisticsSerializer(serializers.Serializer):
    """Serializer for support statistics"""
    
    total_tickets = serializers.IntegerField()
    open_tickets = serializers.IntegerField()
    in_progress_tickets = serializers.IntegerField()
    resolved_tickets = serializers.IntegerField()
    closed_tickets = serializers.IntegerField()
    urgent_tickets = serializers.IntegerField()
    high_priority_tickets = serializers.IntegerField()
    average_response_time = serializers.FloatField()
    customer_satisfaction = serializers.FloatField() 