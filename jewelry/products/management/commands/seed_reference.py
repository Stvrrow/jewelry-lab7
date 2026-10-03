from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from products.models import Client, JewelryType, Material


class Command(BaseCommand):
    help = 'Заполняет справочники: материалы, типы изделий, клиенты'

    def handle(self, *args, **options):
        materials = [
            ('Платина 950', Material.METAL, 3200), ('Золото 585', Material.METAL, 6500),
            ('Золото 750', Material.METAL, 8300), ('Серебро 925', Material.METAL, 110),
            ('Бриллиант 0,1 карат', Material.STONE, 45000), ('Сапфир 0,5 карат', Material.STONE, 18000),
            ('Изумруд 0,3 карат', Material.STONE, 21000), ('Рубин 0,3 карат', Material.STONE, 19500),
        ]
        for name, kind, price in materials:
            Material.objects.get_or_create(name=name, defaults={'kind': kind, 'price': price})
        for name in ('Серьги', 'Кольца', 'Броши', 'Браслеты'):
            JewelryType.objects.get_or_create(name=name)
        clients = [
            ('ivanova', 'Елена', 'Иванова', '+7 916 111-22-33', True, 10),
            ('petrov', 'Сергей', 'Петров', '+7 903 444-55-66', False, 0),
            ('smirnova', 'Ольга', 'Смирнова', '+7 925 777-88-99', True, 5),
        ]
        for username, first, last, phone, regular, discount in clients:
            user, created = User.objects.get_or_create(username=username,
                                                       defaults={'first_name': first, 'last_name': last})
            if created:
                user.set_password('Client2026!')
                user.save()
            Client.objects.get_or_create(user=user, defaults={'phone': phone, 'is_regular': regular,
                                                              'discount': discount})
        self.stdout.write('Справочники заполнены: %d материалов, %d типа изделий, %d клиента' % (
            Material.objects.count(), JewelryType.objects.count(), Client.objects.count()))
