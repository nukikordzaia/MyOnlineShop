from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import  permission_classes, action
from shop.models import Category, Product, Cart
from shop.permissions import IsAdmin
from shop.serializers import CategorySerializer, ProductSerializer, ProductDetSerializer, CartSerializer


class CategoryList(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    # permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'price']

    @permission_classes([IsAdmin])
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductSerializer
        return ProductDetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # @action(detail=True, methods= ['post'], permission_classes=[IsAdmin])
    # def addToCart(self):


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
