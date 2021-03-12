import json

from django.db.models import Sum, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import  permission_classes, action
from shop.models import Category, Product, Cart, CartItem
from shop.permissions import IsAdmin
from shop.serializers import CategorySerializer, ProductSerializer, ProductDetSerializer, CartSerializer, \
    CartItemSerializer, CartItemDetSerializer


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_classes = {
        'list': ProductSerializer,
        'retrieve': ProductDetSerializer,
    }
    default_serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'price']

    # @TODO permissioni rato ar mushaobs
    @permission_classes([IsAdmin])
    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    @permission_classes([IsAdmin])
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#@TODO shevamocmo slug
    @action(detail=True, methods=['get', 'post'], permission_classes=[IsAdmin])
    def addToCart(self, request):
        serializer = CartItemDetSerializer(data=request.data)
        return serializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated])
    def checkout(self, request):
        total_price = request.user.cart.get_total_price()
        import requests
        data: dict = {
            'text': f'Nuki: Total Price {total_price}'
        }
        headers = {
            'Content-type': 'application/json',
        }

        response = requests.post(
            'https://hooks.slack.com/services/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',
            headers=headers,
            data=json.dumps(data)
        )


        return Response(response, status=response.status_code)






