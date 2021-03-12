from django.db.models import ExpressionWrapper, F, DecimalField, Sum
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from shop.models import Category, Product, Cart, CartItem, Tag


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# serializer when showing a list
class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


# serializer when showing a detail
class ProductDetSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price']


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


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
