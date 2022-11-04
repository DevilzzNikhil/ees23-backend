from django.test import SimpleTestCase
from django.urls import reverse, resolve
from custom_auth.views import (
    LoginView,
    LogoutView,
    UserUpdateView,
    RegisterView,
    RequestPasswordResetEmail,
    NewPasswordView,
)


class TestUrls(SimpleTestCase):
    def test_login_url(self):
        login_url = reverse("login")
        self.assertEqual(resolve(login_url).func.view_class, LoginView)

    def test_logut_url(self):
        logout_url = reverse("logout")
        self.assertEqual(resolve(logout_url).func.view_class, LogoutView)

    def test_update_url(self):
        update_url = reverse("update")
        self.assertEqual(resolve(update_url).func.view_class, UserUpdateView)

    def test_register_url_is_resolved(self):
        register_url = reverse("register")
        self.assertEqual(resolve(register_url).func.view_class, RegisterView)

    def test_password_reset_email_url_is_resolved(self):
        password_reset_email_url = reverse("password-reset-email")
        self.assertEqual(
            resolve(password_reset_email_url).func.view_class, RequestPasswordResetEmail
        )

    def test_password_reset_complete_url_is_resolved(self):
        password_reset_complete_url = reverse("password-reset-complete")
        self.assertEqual(
            resolve(password_reset_complete_url).func.view_class, NewPasswordView
        )
