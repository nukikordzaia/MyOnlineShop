from django.db import models
from django.db.models import Model, SlugField, DecimalField, CharField, ForeignKey, TextField, BooleanField, ManyToManyField, \
    IntegerField, OneToOneField


class Category(Model):
    title = models.CharField(max_length=100, blank=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', ]


class Product(Model):
    category = ForeignKey(to='shop.Category', on_delete=models.PROTECT)
    title = CharField(max_length=100, blank=False)
    slug = SlugField(max_length=100)
    price = DecimalField(max_digits=5, decimal_places=2, blank=False)
    description = TextField()
    is_published = BooleanField(default=True)

    def __str__(self):
        return self.title


class Tag(Model):
    title = CharField(max_length=100, blank=False)
    products = ManyToManyField(
        to='shop.Product',
        related_name='tags',
        blank=True,
    )

    def __str__(self):
        return self.title


class CartItem(Model):
    product = ForeignKey(to='shop.Product', related_name='cart_products', blank=False, on_delete=models.CASCADE)
    cart = ForeignKey(to='shop.Cart', related_name='items', blank=False, on_delete=models.PROTECT)
    quantity = IntegerField()
    active = BooleanField(default=True)


class Cart(Model):
    owner = OneToOneField(to='user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.owner
