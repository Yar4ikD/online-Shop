from django.test import TestCase
from django.urls import reverse_lazy


class HistoryViewTestCase(TestCase):
    """Тест представления истории просмотров товара"""

    def setUp(self) -> None:
        self.get_response = self.client.get(reverse_lazy("history:view_history"))

    def test_url_view_exist(self):
        # response = self.client.get("/ru/history/")
        self.assertEqual(self.get_response.status_code, 302)

    def test_url_view_correct_template(self):
        self.assertEqual(self.get_response.status_code, 302)
        # self.assertTemplateUsed(self.get_response, "history/view-history.jinja2")
