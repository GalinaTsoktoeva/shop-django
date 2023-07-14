from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=200, unique=True, verbose_name='slug', **NULLABLE)
    content = models.TextField(**NULLABLE, verbose_name='содержимое')
    img = models.ImageField(**NULLABLE, verbose_name='превью')
    data_create = models.DateTimeField(**NULLABLE, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, **NULLABLE, verbose_name='опубликовано')
    count_views = models.IntegerField(**NULLABLE, default=0, verbose_name='просмотры')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


