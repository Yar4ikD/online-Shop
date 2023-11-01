from celery import shared_task
from order.models import Order


@shared_task(name="Фиктивная оплата")
def fictitious_payment(pk, card_number, amount):
    """
    Задача Celery для фиктивной оплаты заказа.
    Проверяет номер карты и оплачивает заказ, если условия соответствуют.

    :param pk: Идентификатор заказа, который нужно оплатить.
    :param card_number: Номер карты, используемый для оплаты.
    :param amount: Сумма к оплате.
    :return: True, если оплата прошла успешно, False в противном случае.
    """
    if len(card_number) == 8 and int(card_number) % 2 == 0 and card_number[-1] != "0":
        Order.objects.filter(pk=pk).update(is_paid=True)
        return True
    else:
        return False
