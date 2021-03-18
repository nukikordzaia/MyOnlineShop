from typing import List

from django.db import transaction
from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from shop.models import Category, Product, Cart, CartItem, Tag


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['title']


class ProductSerializer(ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            tags_data = validated_data.pop('tags', [])
            product = super().create(validated_data)
            tag_list: List[Tag] = [
                Tag(**tag)
                for tag in tags_data
            ]
            if tag_list:
                Tag.objects.bulk_create(tag_list)
                product.tags.add(*tag_list)

        return product


# serializer when showing a detail
class ProductDetSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'tag']


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartItemDetSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity', ]


class CartSerializer(ModelSerializer):
    total_cost = SerializerMethodField()
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = '__all__'

    @staticmethod
    def get_total_cost(obj: Cart):
        return obj.get_total_price()


class OrderSerializer(Serializer):
    id = IntegerField(required=True)
