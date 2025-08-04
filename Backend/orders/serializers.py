from rest_framework import serializers
from .models import Order, OrderStatusUpdate, OrderDocument


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order model"""
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'product_name', 'product_description',
            'quantity', 'unit_price', 'total_price', 'status', 'delivery_status',
            'tracking_number', 'tracking_url', 'delivery_address', 'delivery_phone',
            'delivery_notes', 'order_date', 'estimated_delivery', 'actual_delivery',
            'updated_at'
        ]
        read_only_fields = ['id', 'order_number', 'total_price', 'order_date', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new orders"""
    
    class Meta:
        model = Order
        fields = [
            'product_name', 'product_description', 'quantity', 'unit_price',
            'delivery_address', 'delivery_phone', 'delivery_notes'
        ]
    
    def validate(self, attrs):
        # Validate quantity
        if attrs.get('quantity', 0) <= 0:
            raise serializers.ValidationError("Miqdor 0 dan katta bo'lishi kerak")
        
        # Validate unit price
        if attrs.get('unit_price', 0) <= 0:
            raise serializers.ValidationError("Narx 0 dan katta bo'lishi kerak")
        
        return attrs


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating orders (admin only)"""
    
    class Meta:
        model = Order
        fields = [
            'status', 'delivery_status', 'tracking_number', 'tracking_url',
            'estimated_delivery', 'actual_delivery', 'admin_notes'
        ]


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for order status updates"""
    
    class Meta:
        model = OrderStatusUpdate
        fields = [
            'id', 'order', 'status', 'delivery_status', 'notes',
            'updated_by', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_by', 'updated_at']


class OrderDocumentSerializer(serializers.ModelSerializer):
    """Serializer for order documents"""
    
    class Meta:
        model = OrderDocument
        fields = [
            'id', 'order', 'document_type', 'title', 'file',
            'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class OrderDetailSerializer(serializers.ModelSerializer):
    """Detailed order serializer with related data"""
    
    status_updates = OrderStatusUpdateSerializer(many=True, read_only=True)
    documents = OrderDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'product_name', 'product_description',
            'quantity', 'unit_price', 'total_price', 'status', 'delivery_status',
            'tracking_number', 'tracking_url', 'delivery_address', 'delivery_phone',
            'delivery_notes', 'order_date', 'estimated_delivery', 'actual_delivery',
            'updated_at', 'admin_notes', 'status_updates', 'documents'
        ]
        read_only_fields = ['id', 'order_number', 'total_price', 'order_date', 'updated_at']


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order list view"""
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'product_name', 'quantity', 'total_price',
            'status', 'delivery_status', 'order_date', 'tracking_number'
        ]
        read_only_fields = ['id', 'order_number', 'total_price', 'order_date']


class OrderStatusUpdateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating status updates"""
    
    class Meta:
        model = OrderStatusUpdate
        fields = ['order', 'status', 'delivery_status', 'notes']
    
    def validate(self, attrs):
        order = attrs.get('order')
        status = attrs.get('status')
        delivery_status = attrs.get('delivery_status')
        
        # Validate that order exists and belongs to user (for non-admin users)
        request = self.context.get('request')
        if request and not request.user.is_staff:
            if order.user != request.user:
                raise serializers.ValidationError("Bu buyurtmani yangilash huquqingiz yo'q")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data) 