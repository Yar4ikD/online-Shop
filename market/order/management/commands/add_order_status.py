from order.models import OrderStatus
from django.core.management import BaseCommand


ORDER_STATUS_NAMES = ["создан", "оплачен", "доставляется", "завершен", "отменен"]


class Command(BaseCommand):
    """Команда для создания статусов заказов"""

    def handle(self, *args, **options):
        self.stdout.write("Создаем статусы заказа...")
        for status in ORDER_STATUS_NAMES:
            order_status, created = OrderStatus.objects.get_or_create(name=status, defaults={"name": status})
        self.stdout.write("Успешно создано!")
