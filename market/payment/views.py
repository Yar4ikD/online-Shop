from payment.functions import fictitious_payment
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from order.models import Order
from .serializers import OrderSerializer


class Payment(ViewSet):
    """
    ViewSet для обработки оплаты заказа.
    Предоставляет методы для просмотра информации о заказе и проведения фиктивной оплаты.
    """

    queryset = Order.objects.all()

    def retrieve(self, request, pk):
        """
        Просмотр информации о заказе.

        :param request: Запрос от клиента.
        :param pk: Идентификатор заказа для просмотра.
        :return: JSON с данными заказа.
        """
        order = get_object_or_404(self.queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request):
        """
        Проведение фиктивной оплаты заказа.

        :param request: Запрос от клиента.
        :return: JSON с информацией о результате оплаты.
        """
        pk = request.data.get("order")
        account = request.data.get("account")
        amount = request.data.get("amount")

        if self.queryset.filter(pk=pk, is_paid=False):
            if fictitious_payment(pk, account, amount):
                return Response({"status": "Оплата прошла успешно"})
            return Response({"status": "Оплата не прошла"})
        else:
            return Response({"status": "Заказ не существует или уже оплачен"})
