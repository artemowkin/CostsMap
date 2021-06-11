from rest_framework import serializers

from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
	"""Serializer for Income model"""

	class Meta:
		model = Income
		fields = ('pk', 'incomes_sum', 'owner', 'date')
		read_only_fields = ('pk', 'date', 'owner')
