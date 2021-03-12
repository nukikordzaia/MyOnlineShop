from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'carts', views.CartViewSet)


urlpatterns = [
    path('category/', views.CategoryList.as_view()),
    path('', include(router.urls)),

]
