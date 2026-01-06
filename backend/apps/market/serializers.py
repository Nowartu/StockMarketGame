from rest_framework import serializers
from .models import Order, Company, Transaction
from django.db import transaction
from ..users.models import UserProfile, UserStock
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import redis
from django.db.models import Q


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    canceled = serializers.SerializerMethodField(read_only=True)
    transactions = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Order
        fields = ['url', 'company', 'type', 'amount', 'available', 'price', 'valid_to', 'canceled', 'transactions']
        read_only_fields = ['cancelled']

    def get_canceled(self, obj):
        return obj.canceled

    def get_transactions(self, obj):
        qs = Transaction.objects.filter(Q(order_1=obj) | Q(order_2=obj))
        return TransactionSimpleSerializer(qs, many=True, context={'request': self.context['request']}).data

    def validate(self, data):
        data['available'] = data['amount']
        if not data.get("valid_to"):
            data['valid_to'] = timezone.now() + timedelta(hours=24)
        profile = self.context['request'].user.userprofile
        if data['type'] == Order.OrderType.BUY:
            cost = data['amount'] * data['price']
            if profile.balance - profile.blocked_balance < cost:
                raise serializers.ValidationError("Insufficient funds!!!")
        elif data['type'] == Order.OrderType.SELL:
            user_stocks = profile.userstock_set.filter(company=data['company']).first()
            if user_stocks.amount - user_stocks.blocked < data['amount']:
                raise serializers.ValidationError("User do not have that much stocks.")
        return data

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be > 0.')
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be > 0.')
        return value

    def validate_valid_to(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError({"valid_to": 'Value must not be in the past.'})
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        profile = user.userprofile

        if validated_data['type'] == Order.OrderType.BUY:
            with transaction.atomic():
                profile = UserProfile.objects.select_for_update().get(pk=profile.pk)
                cost = validated_data['amount'] * validated_data['price']

                if profile.balance - profile.blocked_balance < cost:
                    raise serializers.ValidationError("Insufficient funds.")

                profile.blocked_balance += cost
                profile.save(update_fields=['blocked_balance'])

        elif validated_data['type'] == Order.OrderType.SELL:
            with transaction.atomic():
                user_stocks = UserStock.objects.select_for_update().get(company=validated_data['company'], user_id=profile.pk)

                if user_stocks.amount - user_stocks.blocked < validated_data['amount']:
                    raise serializers.ValidationError("Insufficient stocks.")

                user_stocks.blocked += validated_data['amount']
                user_stocks.save(update_fields=['blocked'])

        order = Order.objects.create(
            user=profile,
            **validated_data
        )

        r = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            password=settings.REDIS_PASSWORD
        )

        r.publish('new_order', order.pk)

        return order


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ['url', 'name', 'full_name', 'sector', 'stock_no', 'market_value', 'value']


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    order = serializers.SerializerMethodField()
    class Meta:
        model = Transaction
        fields = ['url', 'order', 'amount', 'price', 'executed_at']

    def get_order(self, obj):
        user = self.context['request'].user.userprofile
        if obj.order_1.user == user:
            return obj.order_1.pk
        else:
            return obj.order_2.pk


class TransactionSimpleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ['url', 'price', 'amount', 'executed_at']