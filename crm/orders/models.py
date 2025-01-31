from django.core.validators import MaxValueValidator
from django.db import models

from pytils.translit import slugify


class Table(models.Model):
    class TableNumber(models.IntegerChoices):
        FIRST = 1, '1'
        SECOND = 2, '2'
        THIRD = 3, '3'
        FOURTH = 4, '4'
        FIFTH = 5, '5'
        SIXTH = 6, '6'

    number = models.IntegerField(
        choices=TableNumber.choices,
        verbose_name='Номер стола',
        help_text='Укажите номер стола.',
        unique=True
    )

    class Meta:
        verbose_name = 'стол заказов'
        verbose_name_plural = 'Столы заказов'
        ordering = ('number',)

    def __str__(self):
        return f'{self.number} стол'


class BaseCategoryDishModel(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=256,
        verbose_name='Идентификатор',
        help_text=('Может содержать символы латиницы, '
                   'цифры, дефис, подчёркивание.'),
        unique=True,
        blank=True
    )

    class Meta:
        abstract = True
        ordering = ('title',)

    def __str__(self):
        return self.title

    def generate_unique_slug(self):
        initial_slug = slugify(self.title)
        unique_slug = initial_slug
        n = 1
        while True:
            if not self.__class__.objects.filter(slug=unique_slug).exists():
                return unique_slug
            unique_slug = f'{initial_slug}-{n}'
            n += 1

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            self.slug = self.generate_unique_slug()
        return super().save(*args, **kwargs)


class Category(BaseCategoryDishModel):
    class Meta(BaseCategoryDishModel.Meta):
        verbose_name = 'категорию меню'
        verbose_name_plural = 'Категории меню'


class Dish(BaseCategoryDishModel):
    price = models.PositiveIntegerField(
        verbose_name='Цена'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='dishes'
    )

    class Meta(BaseCategoryDishModel.Meta):
        verbose_name = 'блюдо'
        verbose_name_plural = 'Меню'


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        ACCEPTED = 'accepted', 'в ожидании'
        READY = 'ready', 'готово'
        PAID = 'paid', 'оплачено'

    table_number = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name='Номер стола'
    )
    items = models.ManyToManyField(
        Dish,
        through='DishOrder',
        verbose_name='Блюда'
        )

    status = models.CharField(
        max_length=16,
        choices=OrderStatus.choices,
        default=OrderStatus.ACCEPTED,
        verbose_name='Статус заказа'
    )
    created_at = models.DateTimeField(
        verbose_name='Время заказа',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'
        ordering = (
            '-created_at',
        )
        default_related_name = 'orders'

    def __str__(self):
        return f'Заказ {self.id}'


class DishOrder(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
        related_name='order_dishes'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        verbose_name='Блюдо',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Кол-во',
        validators=[MaxValueValidator(32767)]
    )

    class Meta:
        verbose_name = 'блюдо'
        verbose_name_plural = 'блюда'
        ordering = ('order',)

    def __str__(self):
        return self.dish.title
