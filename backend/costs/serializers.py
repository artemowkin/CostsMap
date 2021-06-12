from rest_framework import serializers

from categories.serializers import CategorySerializer
from .models import Cost


class MutableCostSerializer(serializers.ModelSerializer):
    """Serializer for changing/updating Cost model"""

    class Meta:
        model = Cost
        fields = ('pk', 'title', 'costs_sum', 'category', 'owner', 'date')
        read_only_fields = ('pk', 'owner')


class ImmutableCostSerializer(serializers.ModelSerializer):
    """Serializer for getting Cost model"""

    category = CategorySerializer()

    class Meta:
        model = Cost
        fields = ('pk', 'title', 'costs_sum', 'category', 'owner', 'date')
        read_only_fields = ('pk', 'owner')
