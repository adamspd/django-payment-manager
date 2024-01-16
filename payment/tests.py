from django.test import TestCase


class UtilityTestCase(TestCase):
    def setUp(self) -> None:
        self.number = 1

    def test_dumb(self):
        self.assertNotEqual(self.number, 2)
