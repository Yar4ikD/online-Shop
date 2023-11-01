from rest_framework import serializers

from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order. Преобразует объекты Order в формат JSON для API.

    - id: Идентификатор заказа.
    - status: Статус заказа, который определяется на основе is_paid.
    """

    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
        )

    @staticmethod
    def get_status(obj):
        """
        Метод для определения статуса заказа.
        Возвращает "Оплачен", если заказ оплачен, и "Не оплачен" в противном случае.

        :param obj: Объект Order, для которого определяется статус.
        :return: Строка, представляющая статус заказа.
        """
        return "Оплачен" if obj.is_paid else "Не оплачен"
