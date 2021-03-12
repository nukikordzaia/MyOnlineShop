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


class CartSerializer(ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
