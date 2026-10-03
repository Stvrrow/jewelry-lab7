from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Material(models.Model):
    """Материал, с которым работает мастерская: металл или драгоценный камень."""
    METAL = 'metal'
    STONE = 'stone'
    KINDS = [(METAL, 'Металл'), (STONE, 'Драгоценный камень')]

    name = models.CharField('название', max_length=100, unique=True)
    kind = models.CharField('вид', max_length=10, choices=KINDS)
    # для металлов — цена за грамм, для камней — цена за штуку
    price = models.DecimalField('цена за единицу, руб.', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
        ordering = ['kind', 'name']

    def unit(self):
        return 'г' if self.kind == self.METAL else 'шт.'

    def __str__(self):
        return '%s (%s руб./%s)' % (self.name, self.price, self.unit())


class JewelryType(models.Model):
    """Тип изделия: серьги, кольца, броши, браслеты."""
    name = models.CharField('название', max_length=50, unique=True)

    class Meta:
        verbose_name = 'тип изделия'
        verbose_name_plural = 'типы изделий'

    def __str__(self):
        return self.name


class Client(models.Model):
    """Клиент мастерской. Постоянным клиентам предоставляется скидка."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='пользователь')
    phone = models.CharField('телефон', max_length=20, blank=True)
    is_regular = models.BooleanField('постоянный клиент', default=False)
    discount = models.PositiveSmallIntegerField('скидка, %', default=0)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def current_discount(self):
        return self.discount if self.is_regular else 0

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Jewelry(models.Model):
    """Ювелирное изделие, изготавливаемое на заказ."""
    title = models.CharField('название', max_length=200)
    jewelry_type = models.ForeignKey(JewelryType, on_delete=models.PROTECT, verbose_name='тип')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='заказчик')
    text = models.TextField('описание')
    weight = models.DecimalField('вес, г', max_digits=7, decimal_places=2)
    work_price = models.DecimalField('стоимость работы, руб.', max_digits=10, decimal_places=2)
    materials = models.ManyToManyField(Material, through='Composition', verbose_name='материалы')
    created_date = models.DateField('дата заказа', auto_now_add=True)

    class Meta:
        verbose_name = 'изделие'
        verbose_name_plural = 'изделия'
        ordering = ['-created_date', '-id']

    def __str__(self):
        return "%s: %s" % (self.customer.username, self.title)

    def get_excerpt(self):
        return self.text[:140] + "..." if len(self.text) > 140 else self.text
    get_excerpt.short_description = 'описание'

    def materials_price(self):
        return sum((c.cost() for c in self.composition_set.all()), Decimal('0'))

    def full_price(self):
        """Цена изделия: стоимость материалов + стоимость работы."""
        return (self.materials_price() + self.work_price).quantize(Decimal('0.01'))
    full_price.short_description = 'цена без скидки'

    def discount(self):
        client = Client.objects.filter(user=self.customer).first()
        return client.current_discount() if client else 0

    def get_price(self):
        """Итоговая цена с учётом скидки постоянного клиента."""
        price = self.full_price() * (100 - self.discount()) / 100
        return price.quantize(Decimal('0.01'))
    get_price.short_description = 'цена со скидкой'

    def materials_list(self):
        return ', '.join(c.material.name for c in self.composition_set.select_related('material'))
    materials_list.short_description = 'материалы'


class Composition(models.Model):
    """Состав изделия: какой материал и в каком количестве в него входит."""
    jewelry = models.ForeignKey(Jewelry, on_delete=models.CASCADE, verbose_name='изделие')
    material = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name='материал')
    amount = models.DecimalField('количество (г или шт.)', max_digits=7, decimal_places=2)

    class Meta:
        verbose_name = 'материал изделия'
        verbose_name_plural = 'состав изделия'
        unique_together = ('jewelry', 'material')

    def cost(self):
        return (self.material.price * self.amount).quantize(Decimal('0.01'))

    def __str__(self):
        return '%s — %s %s' % (self.material.name, self.amount, self.material.unit())
