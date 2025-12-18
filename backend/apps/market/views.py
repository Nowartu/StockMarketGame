from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .serializers import OrderSerializer
from .models import Order


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Order.objects.all()

    def perform_create(self, serializer):
        order = serializer.save()

        return Response({'order_id': order.id, "status": 'accepted'}, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.canceled = True
        instance.canceled_at = timezone.now()
        instance.save()

        return Response({'order_id': instance.pk, "status": 'accepted'}, status=status.HTTP_204_NO_CONTENT)