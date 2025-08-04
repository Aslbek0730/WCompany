from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template
# from weasyprint import HTML
import os

from .models import Declaration, DeclarationDocument, DeclarationStatusUpdate
from .serializers import (
    DeclarationSerializer, DeclarationCreateSerializer, DeclarationUpdateSerializer,
    DeclarationDetailSerializer, DeclarationListSerializer, DeclarationStatusUpdateSerializer,
    DeclarationDocumentSerializer, DeclarationStatusUpdateCreateSerializer
)


class DeclarationListView(generics.ListCreateAPIView):
    """List and create declarations"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Declaration.objects.all()
        return Declaration.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeclarationCreateSerializer
        return DeclarationListSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeclarationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete declaration"""
    serializer_class = DeclarationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Declaration.objects.all()
        return Declaration.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            if self.request.user.is_staff:
                return DeclarationUpdateSerializer
        return DeclarationDetailSerializer
    
    def perform_update(self, serializer):
        declaration = self.get_object()
        
        # Create status update if status changed
        if 'status' in serializer.validated_data:
            new_status = serializer.validated_data['status']
            if new_status != declaration.status:
                DeclarationStatusUpdate.objects.create(
                    declaration=declaration,
                    status=new_status,
                    updated_by=self.request.user,
                    notes=f"Holat yangilandi: {self.request.user.get_full_name() or self.request.user.username}"
                )
                
                # Update timestamps based on status
                if new_status == 'submitted' and not declaration.submitted_at:
                    declaration.submitted_at = timezone.now()
                elif new_status in ['approved', 'rejected'] and not declaration.reviewed_at:
                    declaration.reviewed_at = timezone.now()
                    declaration.reviewed_by = self.request.user
                elif new_status == 'completed' and not declaration.completed_at:
                    declaration.completed_at = timezone.now()
        
        serializer.save()


class DeclarationStatusUpdateView(generics.ListCreateAPIView):
    """List and create declaration status updates"""
    serializer_class = DeclarationStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        declaration_id = self.kwargs.get('declaration_id')
        if self.request.user.is_staff:
            return DeclarationStatusUpdate.objects.filter(declaration_id=declaration_id)
        return DeclarationStatusUpdate.objects.filter(
            declaration_id=declaration_id,
            declaration__user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DeclarationStatusUpdateCreateSerializer
        return DeclarationStatusUpdateSerializer
    
    def perform_create(self, serializer):
        declaration_id = self.kwargs.get('declaration_id')
        declaration = Declaration.objects.get(id=declaration_id)
        serializer.save(declaration=declaration, updated_by=self.request.user)


class DeclarationDocumentView(generics.ListCreateAPIView):
    """List and create declaration documents"""
    serializer_class = DeclarationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        declaration_id = self.kwargs.get('declaration_id')
        if self.request.user.is_staff:
            return DeclarationDocument.objects.filter(declaration_id=declaration_id)
        return DeclarationDocument.objects.filter(
            declaration_id=declaration_id,
            declaration__user=self.request.user
        )
    
    def perform_create(self, serializer):
        declaration_id = self.kwargs.get('declaration_id')
        declaration = Declaration.objects.get(id=declaration_id)
        serializer.save(declaration=declaration)


class DeclarationDocumentDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve and delete declaration document"""
    serializer_class = DeclarationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return DeclarationDocument.objects.all()
        return DeclarationDocument.objects.filter(declaration__user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def submit_declaration(request, declaration_id):
    """Submit a declaration for review"""
    try:
        if request.user.is_staff:
            declaration = Declaration.objects.get(id=declaration_id)
        else:
            declaration = Declaration.objects.get(id=declaration_id, user=request.user)
    except Declaration.DoesNotExist:
        return Response({'error': 'Deklaratsiya topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if declaration.status != 'draft':
        return Response({'error': 'Faqat qoralama holatidagi deklaratsiyani yuborish mumkin'}, status=status.HTTP_400_BAD_REQUEST)
    
    declaration.status = 'submitted'
    declaration.submitted_at = timezone.now()
    declaration.save()
    
    # Create status update
    DeclarationStatusUpdate.objects.create(
        declaration=declaration,
        status='submitted',
        updated_by=request.user,
        notes=f"Deklaratsiya yuborildi: {request.user.get_full_name() or request.user.username}"
    )
    
    return Response({'message': 'Deklaratsiya yuborildi'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def approve_declaration(request, declaration_id):
    """Approve a declaration (admin only)"""
    try:
        declaration = Declaration.objects.get(id=declaration_id)
    except Declaration.DoesNotExist:
        return Response({'error': 'Deklaratsiya topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if declaration.status != 'submitted':
        return Response({'error': 'Faqat yuborilgan deklaratsiyani tasdiqlash mumkin'}, status=status.HTTP_400_BAD_REQUEST)
    
    declaration.status = 'approved'
    declaration.reviewed_at = timezone.now()
    declaration.reviewed_by = request.user
    declaration.save()
    
    # Create status update
    DeclarationStatusUpdate.objects.create(
        declaration=declaration,
        status='approved',
        updated_by=request.user,
        notes=f"Deklaratsiya tasdiqlandi: {request.user.get_full_name() or request.user.username}"
    )
    
    return Response({'message': 'Deklaratsiya tasdiqlandi'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def reject_declaration(request, declaration_id):
    """Reject a declaration (admin only)"""
    rejection_reason = request.data.get('rejection_reason', '')
    
    try:
        declaration = Declaration.objects.get(id=declaration_id)
    except Declaration.DoesNotExist:
        return Response({'error': 'Deklaratsiya topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if declaration.status not in ['submitted', 'under_review']:
        return Response({'error': 'Bu deklaratsiyani rad etish mumkin emas'}, status=status.HTTP_400_BAD_REQUEST)
    
    declaration.status = 'rejected'
    declaration.rejection_reason = rejection_reason
    declaration.reviewed_at = timezone.now()
    declaration.reviewed_by = request.user
    declaration.save()
    
    # Create status update
    DeclarationStatusUpdate.objects.create(
        declaration=declaration,
        status='rejected',
        updated_by=request.user,
        notes=f"Deklaratsiya rad etildi: {request.user.get_full_name() or request.user.username}. Sabab: {rejection_reason}"
    )
    
    return Response({'message': 'Deklaratsiya rad etildi'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, declaration_id):
    """Generate PDF for declaration"""
    try:
        if request.user.is_staff:
            declaration = Declaration.objects.get(id=declaration_id)
        else:
            declaration = Declaration.objects.get(id=declaration_id, user=request.user)
    except Declaration.DoesNotExist:
        return Response({'error': 'Deklaratsiya topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    # Generate PDF using WeasyPrint
    template = get_template('declarations/declaration_pdf.html')
    context = {
        'declaration': declaration,
        'user': request.user,
    }
    html_content = template.render(context)
    
    # Create PDF
    # pdf = HTML(string=html_content).write_pdf()
    
    # Create response
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="declaration_{declaration.declaration_number}.pdf"'
    
    return response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def declaration_statistics(request):
    """Get declaration statistics for the user"""
    user = request.user
    
    if user.is_staff:
        declarations = Declaration.objects.all()
    else:
        declarations = Declaration.objects.filter(user=user)
    
    total_declarations = declarations.count()
    draft_declarations = declarations.filter(status='draft').count()
    submitted_declarations = declarations.filter(status='submitted').count()
    under_review_declarations = declarations.filter(status='under_review').count()
    approved_declarations = declarations.filter(status='approved').count()
    rejected_declarations = declarations.filter(status='rejected').count()
    completed_declarations = declarations.filter(status='completed').count()
    
    return Response({
        'total_declarations': total_declarations,
        'draft_declarations': draft_declarations,
        'submitted_declarations': submitted_declarations,
        'under_review_declarations': under_review_declarations,
        'approved_declarations': approved_declarations,
        'rejected_declarations': rejected_declarations,
        'completed_declarations': completed_declarations,
    }, status=status.HTTP_200_OK)
