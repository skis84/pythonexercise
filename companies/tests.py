from django.test import TestCase


from companies.validator import Validator


class ValidatorTestCase(TestCase):

    def test_valid_business_id(self):
        self.assertEqual(Validator.is_valid_company_id("1805912-3"), True)

    def test_valid_business_id_old_6_numbers(self):
        self.assertEqual(Validator.is_valid_company_id("116510-6"), True)

    def test_invalid_business_id(self):
        self.assertEqual(Validator.is_valid_company_id("18059123"), False)

    def test_invalid_checksum_in_business_id(self):
        self.assertEqual(Validator.is_valid_company_id("0112039-9"), False)
        self.assertEqual(Validator.is_valid_company_id("1805912-1"), False)
        self.assertEqual(Validator.is_valid_company_id("1805912-0"), False)
