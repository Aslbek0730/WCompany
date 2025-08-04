from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from .models import Order, OrderStatusUpdate, OrderDocument
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateSerializer,
    OrderDetailSerializer, OrderListSerializer, OrderStatusUpdateSerializer,
    OrderDocumentSerializer, OrderStatusUpdateCreateSerializer
)


class OrderListView(generics.ListCreateAPIView):
    """List and create orders"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete order"""
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            if self.request.user.is_staff:
                return OrderUpdateSerializer
        return OrderDetailSerializer
    
    def perform_update(self, serializer):
        order = self.get_object()
        
        # Create status update if status changed
        if 'status' in serializer.validated_data or 'delivery_status' in serializer.validated_data:
            OrderStatusUpdate.objects.create(
                order=order,
                status=serializer.validated_data.get('status', order.status),
                delivery_status=serializer.validated_data.get('delivery_status', order.delivery_status),
                updated_by=self.request.user,
                notes=f"Holat yangilandi: {self.request.user.get_full_name() or self.request.user.username}"
            )
        
        serializer.save()


class OrderStatusUpdateView(generics.ListCreateAPIView):
    """List and create order status updates"""
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if self.request.user.is_staff:
            return OrderStatusUpdate.objects.filter(order_id=order_id)
        return OrderStatusUpdate.objects.filter(
            order_id=order_id,
            order__user=self.request.user
        )
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderStatusUpdateCreateSerializer
        return OrderStatusUpdateSerializer
    
    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        serializer.save(order=order, updated_by=self.request.user)


class OrderDocumentView(generics.ListCreateAPIView):
    """List and create order documents"""
    serializer_class = OrderDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        if self.request.user.is_staff:
            return OrderDocument.objects.filter(order_id=order_id)
        return OrderDocument.objects.filter(
            order_id=order_id,
            order__user=self.request.user
        )
    
    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        order = Order.objects.get(id=order_id)
        serializer.save(order=order)


class OrderDocumentDetailView(generics.RetrieveDestroyAPIView):
    """Retrieve and delete order document"""
    serializer_class = OrderDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderDocument.objects.all()
        return OrderDocument.objects.filter(order__user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_order(request, order_id):
    """Cancel an order"""
    try:
        if request.user.is_staff:
            order = Order.objects.get(id=order_id)
        else:
            order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    if order.status in ['delivered', 'cancelled']:
        return Response({'error': 'Bu buyurtmani bekor qilish mumkin emas'}, status=status.HTTP_400_BAD_REQUEST)
    
    order.status = 'cancelled'
    order.save()
    
    # Create status update
    OrderStatusUpdate.objects.create(
        order=order,
        status='cancelled',
        delivery_status=order.delivery_status,
        updated_by=request.user,
        notes=f"Buyurtma bekor qilindi: {request.user.get_full_name() or request.user.username}"
    )
    
    return Response({'message': 'Buyurtma bekor qilindi'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def order_statistics(request):
    """Get order statistics for the user"""
    user = request.user
    
    if user.is_staff:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=user)
    
    total_orders = orders.count()
    pending_orders = orders.filter(status='pending').count()
    processing_orders = orders.filter(status='processing').count()
    shipped_orders = orders.filter(status='shipped').count()
    delivered_orders = orders.filter(status='delivered').count()
    cancelled_orders = orders.filter(status='cancelled').count()
    
    # Calculate total value
    total_value = sum(order.total_price for order in orders.filter(status__in=['pending', 'processing', 'shipped', 'delivered']))
    
    return Response({
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'total_value': total_value,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def track_order(request, order_id):
    """Track order status and delivery"""
    try:
        if request.user.is_staff:
            order = Order.objects.get(id=order_id)
        else:
            order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Buyurtma topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get latest status update
    latest_update = order.status_updates.first()
    
    tracking_info = {
        'order_number': order.order_number,
        'status': order.status,
        'delivery_status': order.delivery_status,
        'tracking_number': order.tracking_number,
        'tracking_url': order.tracking_url,
        'estimated_delivery': order.estimated_delivery,
        'actual_delivery': order.actual_delivery,
        'latest_update': OrderStatusUpdateSerializer(latest_update).data if latest_update else None,
    }
    
    return Response(tracking_info, status=status.HTTP_200_OK)
