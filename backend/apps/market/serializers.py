from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Order
from django.db import transaction
from ..users.models import UserProfile

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['company', 'type', 'amount', 'price', 'valid_to']

    def validate(self, data):
        data['available'] = data['amount']
        profile = self.context['request'].user.userprofile
        if data['type'] == Order.OrderType.BUY:
            cost = data['amount'] * data['price']
            if profile.balance - profile.blocked_balance < cost:
                raise serializers.ValidationError("Insufficient funds!!!")
        return data

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be > 0.')
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be > 0.')
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        profile = user.userprofile

        with transaction.atomic():
            profile = UserProfile.objects.select_for_update().get(pk=profile.pk)
            cost = validated_data['amount'] * validated_data['price']

            if profile.balance - profile.blocked_balance < cost:
                raise serializers.ValidationError("Insufficient funds.")

            profile.blocked_balance += cost
            profile.save(update_fields=['blocked_balance'])

            order = Order.objects.create(
                user=profile,
                **validated_data
            )

            return order


