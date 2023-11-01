from django.urls import path
from .views import (
    MakeOrderStepOne,
    MakeOrderStepTwo,
    MakeOrderStepThree,
    MakeOrderStepFour,
    PaymentView,
    PaymentProgressView,
    HistoryOrdersView,
    OneOrderView,
    UnsuccessPayment,
    SuccessPayment,
)


app_name = "order"

urlpatterns = [
    path("step_1/", MakeOrderStepOne.as_view(), name="make_order_step_1"),
    path("step_2/", MakeOrderStepTwo.as_view(), name="make_order_step_2"),
    path("step_3/", MakeOrderStepThree.as_view(), name="make_order_step_3"),
    path("step_4/", MakeOrderStepFour.as_view(), name="make_order_step_4"),
    path("payment/<int:order_pk>", PaymentView.as_view(), name="payment"),
    path("payment/progress/<int:order_pk>", PaymentProgressView.as_view(), name="payment_progress"),
    path("done/", SuccessPayment.as_view(), name="payment_success"),
    path("canceled/", UnsuccessPayment.as_view(), name="payment_unsuccess"),
    path("history/", HistoryOrdersView.as_view(), name="history"),
    path("history/<int:order_pk>", OneOrderView.as_view(), name="one_order"),
]
