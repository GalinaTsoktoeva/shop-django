from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание', **NULLABLE)
    img = models.ImageField(upload_to='product/', verbose_name='превью', **NULLABLE)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.PROTECT)
    price = models.IntegerField(verbose_name='Цена')
    data_create = models.DateTimeField(verbose_name='Дата создания', **NULLABLE)
    data_edit = models.DateTimeField(verbose_name='Дата изменения', **NULLABLE)
    user = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE, **NULLABLE)
    is_published = models.BooleanField(default=False, **NULLABLE, verbose_name='опубликовано')

    def __str__(self):
        return f'{self.name} - {self.description}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            (
                "set_published_status",
                "Can publish post"
            )
        ]


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Version(models.Model):

    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    numbers = models.IntegerField(verbose_name='Номер версии')
    name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(default=True, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'

