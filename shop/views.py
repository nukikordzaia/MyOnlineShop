import json

from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shop.models import Category, Product, Cart, CartItem, Tag
from shop.permissions import IsAdmin
from shop.serializers import CategorySerializer, ProductSerializer, ProductDetSerializer, CartSerializer, \
    CartItemDetSerializer, OrderSerializer, TagSerializer


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_classes = {
        'list': ProductSerializer,
        'retrieve': ProductDetSerializer,
        'add_to_cart': CartItemDetSerializer,
    }
    default_serializer_class = ProductSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'price']

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated], url_path='addToCart')
    def add_to_cart(self, request, **_):
        max_order = request.user.cart.items.aggregate(maximum_order=Max('order')).get('maximum_order')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(product=self.get_object(),
                        cart_id=self.request.user.cart.pk,
                        order=max_order + 1,
                        active=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def reorder_items(self, request):
        serializer = OrderSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        l = []
        for order, item in enumerate(serializer.validated_data, start=1):
            print(order, item)
            cartitem = CartItem(id=item['id'], order=order)
            l.append(cartitem)
        CartItem.objects.bulk_update(l, ['order'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

