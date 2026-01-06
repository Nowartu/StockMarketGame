from django.utils import timezone
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from .serializers import OrderSerializer, CompanySerializer, TransactionSerializer
from .models import Order, Company, Transaction
from django.db.models import Q

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwner, DjangoModelPermissions]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user.userprofile, done=False, canceled=False)

    def perform_create(self, serializer):
        order = serializer.save()

        return Response({'order_id': order.id, "status": 'accepted'}, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.canceled = True
        instance.canceled_at = timezone.now()
        instance.save()

        return Response({'order_id': instance.pk, "status": 'accepted'}, status=status.HTTP_204_NO_CONTENT)


class CompanyList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [DjangoModelPermissions]


class TransactionList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [DjangoModelPermissions]
    def get_queryset(self):
        user = self.request.user.userprofile
        orders = Order.objects.filter(user=user)
        transactions = [x.transactions1 for x in orders]
        transactions += [x.transactions2 for x in orders]
        return Transaction.objects.filter(Q(order_1__user=user) | Q(order_2__user=user)).all()