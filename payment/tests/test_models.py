from django.test import TestCase


class UtilityTestCase(TestCase):
    # Test cases for generate_random_id

    def setUp(self) -> None:
        self.number = 1

    def test_dumb(self):
        self.assertNotEqual(self.number, 2)
