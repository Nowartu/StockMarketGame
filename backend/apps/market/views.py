from django.utils import timezone
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, DjangoModelPermissions
from .serializers import OrderSerializer, CompanySerializer, TransactionSerializer, ProfileSerializer, UserStockSerializer, StockSerializer
from .models import Order, Company, Transaction, Stock
from apps.events.models import Event
from django.db.models import Q
from django.db import transaction
from ..users.models import UserProfile, UserStock
from datetime import date


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.user == request.user


class ProfileList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwner, DjangoModelPermissions]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

class UserStockList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserStockSerializer
    permission_classes = [IsOwner, DjangoModelPermissions]

    def get_queryset(self):
        return UserStock.objects.filter(user=self.request.user.userprofile)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwner, DjangoModelPermissions]

    def get_queryset(self):
        done = self.request.query_params.get('done', False)
        canceled = self.request.query_params.get('canceled', False)
        return Order.objects.filter(user=self.request.user.userprofile, done=done, canceled=canceled)

    def perform_create(self, serializer):
        order = serializer.save()

        return Response({'order_id': order.id, "status": 'accepted'}, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        with transaction.atomic():
            profile = instance.user
            if instance.type == "BUY":
                profile.blocked_balance -= instance.available * instance.price
                profile.save(update_fields=["blocked_balance"])

            elif instance.type == "SELL":
                user_stock = profile.userstock.get(company=instance.company)
                user_stock.blocked -= instance.available
                user_stock.save(update_fields=['blocked'])

            instance.canceled = True
            instance.canceled_at = timezone.now()
            instance.save()

            event = Event.objects.create(
                type="CANCEL ORDER",
                source="ORDER",
                reference_id=instance.pk,
                payload={
                    "user": instance.user.nickname,
                }
            )

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


class StockList(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = StockSerializer
    permissions = [DjangoModelPermissions]

    def get_queryset(self):
        d = self.request.query_params.get('date', date.today())
        return Stock.objects.filter(date=d)