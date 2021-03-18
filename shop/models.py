from decimal import Decimal
from django.db import models
from django.db.models import Model, SlugField, DecimalField, CharField, ForeignKey, TextField, BooleanField, \
    ManyToManyField, \
    IntegerField, OneToOneField, ExpressionWrapper, F, Sum, PositiveIntegerField
from django.template.defaultfilters import slugify


class Category(Model):
    title = models.CharField(max_length=100, blank=False)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order', ]


class Product(Model):
    category = ForeignKey(to='shop.Category', on_delete=models.PROTECT)
    tags = ManyToManyField(to='shop.Tag', related_name='products', null=True, blank=True)
    title = CharField(max_length=100, blank=False)
    slug = SlugField(max_length=100, blank=True, null=True)
    price = DecimalField(max_digits=5, decimal_places=2, blank=False)
    description = TextField()
    is_published = BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class Tag(Model):
    title = CharField(max_length=100, blank=False)

    def __str__(self):
        return self.title


class CartItem(Model):
    product = ForeignKey(to='shop.Product', related_name='cart_products', blank=False, on_delete=models.CASCADE)
    cart = ForeignKey(to='shop.Cart', related_name='items', blank=False, on_delete=models.PROTECT)
    quantity = IntegerField()
    active = BooleanField(default=True)
    order = PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', ]


class Cart(Model):
    owner = OneToOneField(to='user.User', on_delete=models.CASCADE)

    def get_total_price(self) -> Decimal:
        return self.items.annotate(
            price=ExpressionWrapper(
                F('product__price') * F('quantity'), output_field=DecimalField()
            )
        ).aggregate(
            total_cost=Sum('price')
        )['total_cost'] or Decimal(0)


