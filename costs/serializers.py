from rest_framework import serializers

from .models import Cost


class CostSerializer(serializers.ModelSerializer):
    """Serializer for Cost model"""

    class Meta:
        model = Cost
        fields = ('pk', 'title', 'costs_sum', 'category', 'owner', 'date')
        read_only_fields = ('pk', 'owner')
