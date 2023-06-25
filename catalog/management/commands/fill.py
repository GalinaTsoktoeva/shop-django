from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Удаляем все что есть в базе"""
        all_products = Product.objects.all()
        for item in all_products:
            item.delete()

        all_category = Category.objects.all()
        for item_c in all_category:
            item_c.delete()
        """Заполняем базу"""
        category_list = [
            {'id': '1', 'name': 'product', 'description': 'soup'},
            {'id': '2', 'name': 'smartphone', 'description': 'smartphone'}

        ]
        category_for_create = []
        for category_item in category_list:
            category_for_create.append(
                Category(**category_item)
            )
        Category.objects.bulk_create(category_for_create)

        product_list = [
            {'id': '1', 'name': 'soup', 'description': 'soup for baby', 'category': Category.objects.get(pk=1), 'price': '100'},
            {'id': '2', 'name': 'xiomi', 'category': Category.objects.get(pk=2), 'price': '10000'},
            {'id': '3', 'name': 'shower', 'category': Category.objects.get(pk=1), 'price': '300'}
        ]
        products_for_create = []
        for product_item in product_list:
            products_for_create.append(
                Product(**product_item)
            )
        Product.objects.bulk_create(products_for_create)