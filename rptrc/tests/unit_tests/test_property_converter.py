"""
Unit tests for property_converter.py
"""

import pytest

from rptrc.src.operators.property_converter import PropertyConverter
from rptrc.src.etc.exceptions import PropertyConversionException


class TestPropertyConverter:
    """
    Class to run unit tests for property_converter.py
    """

    def test_ensure_valid_conversion_type_when_conversion_type_is_valid(self):
        """
        Tests the ensure_valid_conversion_type method
        when a valid conversion type is passed.
        Test passes if no exceptions are thrown.
        """
        property_converter = PropertyConverter({})
        for conversion_type in ['camelcase_to_uppercase', 'uppercase_to_camelcase']:
            property_converter.ensure_valid_conversion_type(conversion_type)

    def test_ensure_valid_conversion_type_when_conversion_type_is_invalid(self):
        """
        Tests the ensure_valid_conversion_type method
        when an invalid conversion type is passed.
        Test passes if expected exception is thrown.
        """
        property_converter = PropertyConverter({})
        with pytest.raises(PropertyConversionException) as exception:
            property_converter.ensure_valid_conversion_type('fake_conversion_type')
        expected_exception_value = \
            'Property Conversion Exception, "fake_conversion_type" is not a valid conversion type.'
        assert str(exception.value) == expected_exception_value

    def test_ensure_value_is_a_string_when_value_is_a_string(self):
        """
        Tests the ensure_value_is_a_string method
        when a valid type is passed.
        Test passes if no exceptions are thrown.
        """
        property_converter = PropertyConverter({})
        for string in ['these', 'Are', 'A L L', 'strin_gs']:
            property_converter.ensure_value_is_a_string(string)

    def test_ensure_value_is_a_string_when_value_is_not_a_string(self):
        """
        Tests the ensure_value_is_a_string method
        when an invalid type is passed.
        Test passes if expected exception is thrown.
        """
        property_converter = PropertyConverter({})
        for non_string in [123, [1, 2, 3], {1: ":)"}]:
            with pytest.raises(PropertyConversionException) as exception:
                property_converter.ensure_value_is_a_string(non_string)
            expected_exception_value = \
                f'Property Conversion Exception, "{non_string}" is not a string so cannot be converted.'
        assert str(exception.value) == expected_exception_value

    def test_make_first_letter_lowercase_when_first_letter_is_uppercase(self):
        """
        Tests the make_first_letter_lowercase method
        when the first letter is currently uppercase.
        """
        property_converter = PropertyConverter({})
        converted_word = property_converter.make_first_letter_lowercase('Capitalized')
        expected_converted_word = 'capitalized'
        assert converted_word == expected_converted_word

    def test_make_first_letter_lowercase_when_first_letter_is_lowercase(self):
        """
        Tests the make_first_letter_lowercase method
        when the first letter is currently lowercase.
        """
        property_converter = PropertyConverter({})
        converted_word = property_converter.make_first_letter_lowercase('capitalized')
        expected_converted_word = 'capitalized'
        assert converted_word == expected_converted_word

    def test_convert_camelcase_to_uppercase_when_word_is_camelcase(self):
        """
        Tests the convert_camelcase_to_uppercase method
        when the word to be converted is in camelcase.
        """
        property_converter = PropertyConverter({})
        converted_word = property_converter.convert_camelcase_to_uppercase('myCamelCaseProperty')
        expected_converted_word = 'MY_CAMEL_CASE_PROPERTY'
        assert converted_word == expected_converted_word

    def test_convert_camelcase_to_uppercase_when_word_is_uppercase(self):
        """
        Tests the convert_camelcase_to_uppercase method
        when the word to be converted is in uppercase already.
        """
        property_converter = PropertyConverter({})
        converted_word = property_converter.convert_camelcase_to_uppercase('MY_UPPERCASE_PROPERTY')
        expected_converted_word = 'MY_UPPERCASE_PROPERTY'
        assert converted_word == expected_converted_word

    def test_convert_uppercase_to_camelcase_when_word_is_camelcase(self):
        """
        Tests the convert_uppercase_to_camelcase method
        when the word to be converted is in camelcase already.
        """
        property_converter = PropertyConverter({})
        converted_word = property_converter.convert_uppercase_to_camelcase('myCamelCaseProperty')
        expected_converted_word = 'myCamelCaseProperty'
        assert converted_word == expected_converted_word

    def test_convert_uppercase_to_camelcase_when_word_is_uppercase(self):
        """
        Tests the convert_uppercase_to_camelcase method
        when the word to be converted is in uppercase.
        """
        property_converter = PropertyConverter({})
        converted_word = property_converter.convert_uppercase_to_camelcase('MY_UPPERCASE_PROPERTY')
        expected_converted_word = 'myUppercaseProperty'
        assert converted_word == expected_converted_word

    def test_convert_string(self):
        """
        Tests that the convert_string method maps the previously
        tested functionality correctly.
        """
        property_converter = PropertyConverter({})
        converted_to_uppercase = property_converter.convert_string('myStringToConvert', 'camelcase_to_uppercase')
        converted_to_camelcase = property_converter.convert_string('MY_STRING_TO_CONVERT', 'uppercase_to_camelcase')
        assert converted_to_uppercase == 'MY_STRING_TO_CONVERT'
        assert converted_to_camelcase == 'myStringToConvert'

    def test_convert_properties_non_nested(self):
        """
        Tests that the convert_properties method maps the previously
        tested functionality correctly (non-nested variation).
        """
        uppercase_properties = {
            'MY_PROPERTY_ONE': 1,
            'MY_PROPERTY_TWO': 2,
            'MY_PROPERTY_THREE': 3
        }

        camelcase_properties = {
            'myPropertyOne': 1,
            'myPropertyTwo': 2,
            'myPropertyThree': 3
        }

        camel_property_converter = PropertyConverter(camelcase_properties)
        upper_property_converter = PropertyConverter(uppercase_properties)

        converted_to_upper = camel_property_converter.convert_properties('camelcase_to_uppercase')
        converted_to_camel = upper_property_converter.convert_properties('uppercase_to_camelcase')

        assert converted_to_upper == uppercase_properties
        assert converted_to_camel == camelcase_properties

    def test_convert_properties_nested(self):
        """
        Tests that the convert_properties method maps the previously
        tested functionality correctly (nested variation).
        """
        uppercase_properties = {
            'MY_PROPERTY_ONE': 1,
            'MY_PROPERTY_TWO': 2,
            'MY_PROPERTY_THREE': 3,
            'MY_PROPERTY_DICT_ONE': {
                'MY_NESTED_PROPERTY_ONE': 4,
                'MY_NESTED_PROPERTY_TWO': 5,
                'MY_NESTED_PROPERTY_THREE': 6
            },
            'MY_PROPERTY_DICT_TWO': {
                'MY_NESTED_PROPERTY_FOUR': 7,
                'MY_NESTED_PROPERTY_FIVE': 8,
                'MY_NESTED_PROPERTY_SIX': 9
            }
        }

        camelcase_properties = {
            'myPropertyOne': 1,
            'myPropertyTwo': 2,
            'myPropertyThree': 3,
            'myPropertyDictOne': {
                'myNestedPropertyOne': 4,
                'myNestedPropertyTwo': 5,
                'myNestedPropertyThree': 6
            },
            'myPropertyDictTwo': {
                'myNestedPropertyFour': 7,
                'myNestedPropertyFive': 8,
                'myNestedPropertySix': 9
            }
        }

        camel_property_converter = PropertyConverter(camelcase_properties)
        upper_property_converter = PropertyConverter(uppercase_properties)

        converted_to_upper = camel_property_converter.convert_properties('camelcase_to_uppercase')
        converted_to_camel = upper_property_converter.convert_properties('uppercase_to_camelcase')

        assert converted_to_upper == uppercase_properties
        assert converted_to_camel == camelcase_properties
