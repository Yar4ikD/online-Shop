from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.test import TestCase


class UploadFileViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Устанавливает начальные данные для всех тестов.
        Создает суперпользователя и обычного пользователя.
        :return: None
        """
        cls.superuser = User.objects.create_superuser(
            username="superuser", password="testpassword", email="superuser@test.com"
        )
        cls.user = User.objects.create_user(username="user", password="testpassword", email="user@test.com")

        cls.url = reverse("products:upload_file")

    def test_access_user(self):
        """
        Тестирование доступа обычного пользователя.
        :return: None
        """
        self.client.login(username="superuser@test.com", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_access_superuser(self):
        """
        Тестирование доступа суперпользователя.
        :return: None
        """
        self.client.login(username="superuser@test.com", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/upload_file.jinja2")

    def test_form_valid(self):
        """
        Тестирование успешной отправки формы загрузки файла.
        :return: None
        """
        self.client.login(username="superuser@test.com", password="testpassword")
        file_content = b"This is a test file content."
        uploaded_file = SimpleUploadedFile("test_file.txt", file_content)
        response = self.client.post(self.url, {"file": uploaded_file})
        self.assertEqual(response.status_code, 302)
