from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Income


class IncomeSerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Income
        fields = ['pk', 'incomes_sum', 'owner']


class PostIncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = ['incomes_sum', 'owner']
