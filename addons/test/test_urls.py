from django.test import SimpleTestCase
from django.urls import reverse, resolve
from addons.views import (
    Referral_Code_View,
    QueryView,
)


class TestUrls(SimpleTestCase):
    def test_query_url(self):
        query_url = reverse("query")
        self.assertEqual(resolve(query_url).func.view_class, QueryView)

    def test_referral_url(self):
        referral_url = reverse("referral")
        self.assertEqual(resolve(referral_url).func.view_class, Referral_Code_View)
