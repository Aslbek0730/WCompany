from rest_framework import serializers
from .models import Declaration, DeclarationDocument, DeclarationStatusUpdate


class DeclarationSerializer(serializers.ModelSerializer):
    """Serializer for declaration model"""
    
    class Meta:
        model = Declaration
        fields = [
            'id', 'declaration_number', 'declaration_type', 'status',
            'order', 'passport_series', 'passport_number', 'passport_issue_date',
            'passport_expiry_date', 'passport_issuing_authority', 'contact_name',
            'contact_phone', 'contact_email', 'delivery_address', 'delivery_country',
            'delivery_city', 'product_name', 'product_description', 'product_quantity',
            'product_unit', 'product_value', 'product_currency', 'customs_code',
            'customs_value', 'customs_duty', 'notes', 'created_at', 'submitted_at',
            'reviewed_at', 'completed_at', 'updated_at'
        ]
        read_only_fields = ['id', 'declaration_number', 'created_at', 'submitted_at', 'reviewed_at', 'completed_at', 'updated_at']


class DeclarationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new declarations"""
    
    class Meta:
        model = Declaration
        fields = [
            'declaration_type', 'order', 'passport_series', 'passport_number',
            'passport_issue_date', 'passport_expiry_date', 'passport_issuing_authority',
            'contact_name', 'contact_phone', 'contact_email', 'delivery_address',
            'delivery_country', 'delivery_city', 'product_name', 'product_description',
            'product_quantity', 'product_unit', 'product_value', 'product_currency',
            'customs_code', 'customs_value', 'customs_duty', 'notes'
        ]
    
    def validate(self, attrs):
        # Validate passport number format
        passport_series = attrs.get('passport_series', '')
        passport_number = attrs.get('passport_number', '')
        
        if len(passport_series) != 2:
            raise serializers.ValidationError("Pasport seriyasi 2 ta harf bo'lishi kerak")
        
        if len(passport_number) != 7:
            raise serializers.ValidationError("Pasport raqami 7 ta raqam bo'lishi kerak")
        
        if not passport_number.isdigit():
            raise serializers.ValidationError("Pasport raqami faqat raqamlardan iborat bo'lishi kerak")
        
        # Validate product value
        if attrs.get('product_value', 0) <= 0:
            raise serializers.ValidationError("Mahsulot qiymati 0 dan katta bo'lishi kerak")
        
        return attrs


class DeclarationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating declarations (admin only)"""
    
    class Meta:
        model = Declaration
        fields = [
            'status', 'customs_code', 'customs_value', 'customs_duty',
            'admin_notes', 'rejection_reason'
        ]


class DeclarationStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for declaration status updates"""
    
    class Meta:
        model = DeclarationStatusUpdate
        fields = [
            'id', 'declaration', 'status', 'notes', 'updated_by', 'updated_at'
        ]
        read_only_fields = ['id', 'updated_by', 'updated_at']


class DeclarationDocumentSerializer(serializers.ModelSerializer):
    """Serializer for declaration documents"""
    
    class Meta:
        model = DeclarationDocument
        fields = [
            'id', 'declaration', 'document_type', 'title', 'file',
            'description', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class DeclarationDetailSerializer(serializers.ModelSerializer):
    """Detailed declaration serializer with related data"""
    
    status_updates = DeclarationStatusUpdateSerializer(many=True, read_only=True)
    documents = DeclarationDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Declaration
        fields = [
            'id', 'declaration_number', 'declaration_type', 'status',
            'order', 'passport_series', 'passport_number', 'passport_issue_date',
            'passport_expiry_date', 'passport_issuing_authority', 'contact_name',
            'contact_phone', 'contact_email', 'delivery_address', 'delivery_country',
            'delivery_city', 'product_name', 'product_description', 'product_quantity',
            'product_unit', 'product_value', 'product_currency', 'customs_code',
            'customs_value', 'customs_duty', 'notes', 'admin_notes', 'rejection_reason',
            'created_at', 'submitted_at', 'reviewed_at', 'completed_at', 'updated_at',
            'reviewed_by', 'status_updates', 'documents'
        ]
        read_only_fields = ['id', 'declaration_number', 'created_at', 'submitted_at', 'reviewed_at', 'completed_at', 'updated_at']


class DeclarationListSerializer(serializers.ModelSerializer):
    """Serializer for declaration list view"""
    
    class Meta:
        model = Declaration
        fields = [
            'id', 'declaration_number', 'declaration_type', 'status',
            'product_name', 'product_quantity', 'product_value', 'product_currency',
            'created_at', 'submitted_at'
        ]
        read_only_fields = ['id', 'declaration_number', 'created_at', 'submitted_at']


class DeclarationStatusUpdateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating status updates"""
    
    class Meta:
        model = DeclarationStatusUpdate
        fields = ['declaration', 'status', 'notes']
    
    def validate(self, attrs):
        declaration = attrs.get('declaration')
        status = attrs.get('status')
        
        # Validate that declaration exists and belongs to user (for non-admin users)
        request = self.context.get('request')
        if request and not request.user.is_staff:
            if declaration.user != request.user:
                raise serializers.ValidationError("Bu deklaratsiyani yangilash huquqingiz yo'q")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['updated_by'] = self.context['request'].user
        return super().create(validated_data) 