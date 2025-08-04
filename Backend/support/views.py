from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q, Avg, Count
from datetime import timedelta

from .models import SupportTicket, SupportMessage, SupportCategory, SupportTemplate
from .serializers import (
    SupportTicketSerializer, SupportTicketCreateSerializer, SupportTicketUpdateSerializer,
    SupportTicketListSerializer, SupportTicketDetailSerializer, SupportMessageSerializer,
    SupportMessageCreateSerializer, SupportMessageUpdateSerializer, SupportCategorySerializer,
    SupportCategoryCreateSerializer, SupportTemplateSerializer, SupportTemplateCreateSerializer,
    SupportStatisticsSerializer
)


class SupportTicketListView(generics.ListCreateAPIView):
    """List and create support tickets"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SupportTicketCreateSerializer
        return SupportTicketListSerializer


class SupportTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete support ticket"""
    serializer_class = SupportTicketDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            if self.request.user.is_staff:
                return SupportTicketUpdateSerializer
        return SupportTicketDetailSerializer


class SupportMessageListView(generics.ListCreateAPIView):
    """List and create support messages"""
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        if self.request.user.is_staff:
            return SupportMessage.objects.filter(ticket_id=ticket_id)
        return SupportMessage.objects.filter(
            ticket_id=ticket_id,
            ticket__user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SupportMessageCreateSerializer
        return SupportMessageSerializer
    
    def perform_create(self, serializer):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = SupportTicket.objects.get(id=ticket_id)
        serializer.save(ticket=ticket)


class SupportMessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete support message"""
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return SupportMessage.objects.all()
        return SupportMessage.objects.filter(ticket__user=self.request.user)


class SupportCategoryListView(generics.ListCreateAPIView):
    """List and create support categories (admin only)"""
    serializer_class = SupportCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SupportCategory.objects.all()


class SupportCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete support categories (admin only)"""
    serializer_class = SupportCategorySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SupportCategory.objects.all()


class SupportTemplateListView(generics.ListCreateAPIView):
    """List and create support templates (admin only)"""
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return SupportTemplate.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SupportTemplateCreateSerializer
        return SupportTemplateSerializer


class SupportTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete support templates (admin only)"""
    serializer_class = SupportTemplateSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = SupportTemplate.objects.all()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def close_ticket(request, ticket_id):
    """Close a support ticket"""
    try:
        if request.user.is_staff:
            ticket = SupportTicket.objects.get(id=ticket_id)
        else:
            ticket = SupportTicket.objects.get(id=ticket_id, user=request.user)
    except SupportTicket.DoesNotExist:
        return Response({'error': 'Tiket topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if ticket.status in ['closed', 'resolved']:
        return Response({'error': 'Bu tiket allaqachon yopilgan'}, status=status.HTTP_400_BAD_REQUEST)
    
    ticket.status = 'closed'
    ticket.closed_at = timezone.now()
    ticket.save()
    
    # Create system message
    SupportMessage.objects.create(
        ticket=ticket,
        sender=request.user,
        message_type='system',
        message=f"Tiket {request.user.get_full_name() or request.user.username} tomonidan yopildi"
    )
    
    return Response({'message': 'Tiket yopildi'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def resolve_ticket(request, ticket_id):
    """Resolve a support ticket"""
    try:
        if request.user.is_staff:
            ticket = SupportTicket.objects.get(id=ticket_id)
        else:
            ticket = SupportTicket.objects.get(id=ticket_id, user=request.user)
    except SupportTicket.DoesNotExist:
        return Response({'error': 'Tiket topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if ticket.status in ['closed', 'resolved']:
        return Response({'error': 'Bu tiket allaqachon hal qilingan'}, status=status.HTTP_400_BAD_REQUEST)
    
    ticket.status = 'resolved'
    ticket.resolved_at = timezone.now()
    ticket.save()
    
    # Create system message
    SupportMessage.objects.create(
        ticket=ticket,
        sender=request.user,
        message_type='system',
        message=f"Tiket {request.user.get_full_name() or request.user.username} tomonidan hal qilindi"
    )
    
    return Response({'message': 'Tiket hal qilindi'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_message_read(request, message_id):
    """Mark a support message as read"""
    try:
        if request.user.is_staff:
            message = SupportMessage.objects.get(id=message_id)
        else:
            message = SupportMessage.objects.get(id=message_id, ticket__user=request.user)
    except SupportMessage.DoesNotExist:
        return Response({'error': 'Xabar topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    message.is_read = True
    message.read_at = timezone.now()
    message.read_by = request.user
    message.save()
    
    return Response({'message': 'Xabar o\'qilgan deb belgilandi'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def support_statistics(request):
    """Get support statistics"""
    user = request.user
    
    if user.is_staff:
        tickets = SupportTicket.objects.all()
    else:
        tickets = SupportTicket.objects.filter(user=user)
    
    total_tickets = tickets.count()
    open_tickets = tickets.filter(status='open').count()
    in_progress_tickets = tickets.filter(status='in_progress').count()
    resolved_tickets = tickets.filter(status='resolved').count()
    closed_tickets = tickets.filter(status='closed').count()
    urgent_tickets = tickets.filter(priority='urgent').count()
    high_priority_tickets = tickets.filter(priority='high').count()
    
    # Calculate average response time (for staff only)
    average_response_time = None
    if user.is_staff:
        response_times = []
        for ticket in tickets.filter(status__in=['resolved', 'closed']):
            first_message = ticket.messages.filter(message_type='staff').first()
            if first_message:
                response_time = (first_message.created_at - ticket.created_at).total_seconds() / 3600  # hours
                response_times.append(response_time)
        
        if response_times:
            average_response_time = sum(response_times) / len(response_times)
    
    # Calculate customer satisfaction (placeholder)
    customer_satisfaction = 4.5  # This would be calculated from ratings
    
    return Response({
        'total_tickets': total_tickets,
        'open_tickets': open_tickets,
        'in_progress_tickets': in_progress_tickets,
        'resolved_tickets': resolved_tickets,
        'closed_tickets': closed_tickets,
        'urgent_tickets': urgent_tickets,
        'high_priority_tickets': high_priority_tickets,
        'average_response_time': average_response_time,
        'customer_satisfaction': customer_satisfaction,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_tickets(request):
    """Search support tickets"""
    query = request.query_params.get('q', '')
    status_filter = request.query_params.get('status', '')
    priority_filter = request.query_params.get('priority', '')
    
    if request.user.is_staff:
        tickets = SupportTicket.objects.all()
    else:
        tickets = SupportTicket.objects.filter(user=request.user)
    
    if query:
        tickets = tickets.filter(
            Q(subject__icontains=query) |
            Q(description__icontains=query) |
            Q(ticket_number__icontains=query)
        )
    
    if status_filter:
        tickets = tickets.filter(status=status_filter)
    
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)
    
    serializer = SupportTicketListSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
