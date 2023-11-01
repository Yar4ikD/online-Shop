from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile


from profiles.models import Profile


class ProfileViewTestCase(TestCase):
    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/0-user-group-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)
        cls.user_password = "admin27admin"

        cls.log_page = reverse_lazy("profiles:login")
        cls.reg_page = reverse_lazy("profiles:registration_user")

        cls.register_data = {
            "username": "test_name",
            "email": "test_email@email.com",
            "password1": "password1test",
            "password2": "password1test",
            "group": 1,
        }

    def setUp(self):
        self.client = Client()

    def test_get_login_page(self):
        response: TemplateResponse = self.client.get(self.log_page)

        self.assertEqual(200, response.status_code)
        self.assertIn("profiles/login.jinja2", response.template_name)

    def test_login_redirect(self):
        data = {
            "email": self.user.email,
            "password": self.user_password,
        }
        response: HttpResponseRedirect = self.client.post(self.log_page, data=data)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/ru/", response.url)

    def test_login_with_username(self):
        data = {
            "email": self.user.username,
            "password": self.user_password,
        }
        response: TemplateResponse = self.client.post(self.log_page, data=data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_get_register_user_page(self):
        response: TemplateResponse = self.client.get(self.reg_page)

        self.assertEqual(200, response.status_code)
        self.assertIn("profiles/registr.jinja2", response.template_name)

    def test_register_user_profile(self):
        response: HttpResponseRedirect = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(302, response.status_code)
        self.assertEqual("/ru/profile/login/", response.url)

        self.assertTrue(User.objects.filter(email="test_email@email.com").exists())
        self.assertTrue(Profile.objects.filter(user__username="test_name").exists())

    def test_register_not_correct_email(self):
        self.register_data["email"] = "test_email@email"
        response: TemplateResponse = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_register_not_correct_password(self):
        self.register_data["password2"] = "password2test"
        response: TemplateResponse = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())

    def test_register_without_group_password(self):
        self.register_data["group"] = ""
        response: TemplateResponse = self.client.post(self.reg_page, data=self.register_data)

        self.assertEqual(200, response.status_code)
        self.assertFalse(response.context_data["form"].is_valid())


class ProfileModelTestCase(TestCase):
    fixtures = [
        "fixtures/01-user-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)

        cls.data = {
            "user": cls.user,
            "address": "Test address",
            "phone": "+79882666636",
            "balance": 0,
        }

    def test_create_profile(self):
        profile = Profile.objects.create(**self.data)

        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.phone, self.data["phone"])


class ProfileTestCase(TestCase):
    """Тест представления детальной страницы профиля"""

    fixtures = [
        "fixtures/01-user-fixtures.json",
        "fixtures/02-profile-fixtures.json",
    ]

    @classmethod
    def setUpTestData(cls):
        cls.page_url = reverse("profiles:profile")
        cls.user = User.objects.get(pk=8)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_method(self):
        """Тест ответа GET-запроса страницы"""

        response = self.client.get(self.page_url)
        self.assertEqual(200, response.status_code),
        self.assertIn("profiles/profile_update_form.jinja2", response.template_name)

    def test_post_method(self):
        """Тест ответа POST-запроса страницы"""

        data = {
            "first_name": "Кар",
            "last_name": "Карыч",
            "email": "kar_karych@admin.com",
            "phone": "+79999999999",
        }

        expected_user = User.objects.get(pk=8)
        self.assertEqual(expected_user.first_name, data["first_name"])
        self.assertEqual(expected_user.last_name, data["last_name"])
        self.assertEqual(expected_user.email, data["email"])

        expected_profile = Profile.objects.get(user=expected_user)
        self.assertEqual(expected_profile.phone, data["phone"])

    def test_upload_image(self):
        """Тест загрузки изображения"""

        image_path = "media/users/9/user-details/кар-карыч.png"
        with open(image_path, "rb") as img:
            image = SimpleUploadedFile(name="image.png", content=img.read(), content_type="image/png")
            response = self.client.post(self.page_url, data={"avatar": image})
            self.assertEqual(response.status_code, 200)
