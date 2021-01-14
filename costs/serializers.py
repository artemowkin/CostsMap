from rest_framework import serializers

from accounts.serializers import UserSerializer
from .models import Category, Cost


class CategorySerializer(serializers.ModelSerializer):
    owner = UserSerializer()

    class Meta:
        model = Category
        fields = ['pk', 'title', 'owner']


class PostCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['title', 'owner']


class CategoryInCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['pk', 'title']


class CostSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    category = CategoryInCostSerializer()

    class Meta:
        model = Cost
        fields = [
            'pk', 'title', 'costs_sum', 'category', 'owner', 'date',
            'pub_datetime'
        ]


class PostCostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cost
        fields = [
            'title', 'costs_sum', 'category', 'owner'
        ]
