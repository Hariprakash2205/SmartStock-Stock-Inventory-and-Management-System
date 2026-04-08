from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from django.utils import timezone

from .models import Department, StockItem, StockRequest, Transaction
from .serializers import (
    DepartmentSerializer,
    StockItemSerializer,
    StockRequestSerializer,
    TransactionSerializer
)

# ---------------------------
# Department ViewSet
# ---------------------------
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    # ✅ Allow frontend POST without CSRF issues
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]


# ---------------------------
# Stock Item ViewSet
# ---------------------------
class StockItemViewSet(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer
    permission_classes = [AllowAny]


# ---------------------------
# Stock Request ViewSet
# ---------------------------
class StockRequestViewSet(viewsets.ModelViewSet):
    queryset = StockRequest.objects.all().order_by('-requested_at')
    serializer_class = StockRequestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Allow anonymous requests for now (testing mode)
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(requester=user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        stock_request = self.get_object()

        if stock_request.status != 'pending':
            return Response(
                {'error': 'This request has already been processed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item = stock_request.item
        if item.quantity < stock_request.quantity:
            return Response(
                {'error': 'Not enough stock available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.quantity -= stock_request.quantity
        item.save()

        stock_request.status = 'approved'
        stock_request.reviewed_at = timezone.now()
        stock_request.save()

        Transaction.objects.create(
            item=item,
            quantity_changed=-stock_request.quantity,
            performed_by=request.user if request.user.is_authenticated else None,
            note=f"Approved stock request #{stock_request.id}"
        )

        return Response({'message': 'Stock request approved'}, status=200)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        stock_request = self.get_object()

        if stock_request.status != 'pending':
            return Response(
                {'error': 'This request has already been processed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        stock_request.status = 'rejected'
        stock_request.reviewed_at = timezone.now()
        stock_request.save()

        return Response({'message': 'Stock request rejected'}, status=200)


# ---------------------------
# Transaction ViewSet
# ---------------------------
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-timestamp')
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]
