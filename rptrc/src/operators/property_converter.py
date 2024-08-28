"""
The operator for handling the conversion of properties to different formats.
"""
import re
import logging

from rptrc.src.etc.exceptions import PropertyConversionException


class PropertyConverter:
    """
    Class to handle the conversion of properties/variables to different formats.
    """
    VALID_CONVERSION_TYPES = {'camelcase_to_uppercase', 'uppercase_to_camelcase'}

    def __init__(self, properties: dict):
        self.properties = properties

    @staticmethod
    def make_first_letter_lowercase(string):
        """
        Method to make the first letter of a string lowercase.
        :param string:
        :return: string
        :rtype: str
        """
        return f'{string[:1].lower()}{string[1:]}'

    @staticmethod
    def ensure_valid_conversion_type(conversion_type):
        """
        Method to ensure a conversion type is valid.
        :param conversion_type:
        :raises Exception: Raises exception if conversion type is invalid.
        """
        if conversion_type not in PropertyConverter.VALID_CONVERSION_TYPES:
            raise PropertyConversionException(f'"{conversion_type}" is not a valid conversion type.')
        logging.debug(f'{conversion_type} is a valid conversion type.')

    @staticmethod
    def ensure_value_is_a_string(string):
        """
        Method to ensure a value passed is a string.
        :param string:
        :raises Exception: Raises exception if value passed is not a string.
        """
        if not isinstance(string, str):
            raise PropertyConversionException(f'"{string}" is not a string so cannot be converted.')

    @staticmethod
    def convert_camelcase_to_uppercase(string):
        """
        Method to convert from camelcase to uppercase underscore.
        :param string:
        :return: string
        :rtype: str
        """
        string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).upper()

    def convert_uppercase_to_camelcase(self, string):
        """
        Method to convert from uppercase underscore to camelcase.
        :param string:
        :return: string
        :rtype: str
        """
        def is_camel_case(string):
            """
            Helper function to check if a string is camelcase.
            """
            return string != string.lower() and string != string.upper() and "_" not in string

        if is_camel_case(string):
            return string

        capitalized_camel = ''.join(word.title() for word in string.split('_'))
        return self.make_first_letter_lowercase(capitalized_camel)

    def convert_string(self, string, conversion_type):
        """
        Method to convert a string to a different format.
        :param string:
        :param conversion_type:
        :return: converted_string
        :rtype: str
        """
        self.ensure_value_is_a_string(string)
        self.ensure_valid_conversion_type(conversion_type)

        convert = {
            'camelcase_to_uppercase': self.convert_camelcase_to_uppercase,
            'uppercase_to_camelcase': self.convert_uppercase_to_camelcase
        }

        return convert[conversion_type](string)

    def convert_properties(self, conversion_type):
        """
        Method to convert all properties stored in this class and return them.
        :param conversion_type:
        :return: converted_properties
        :rtype: dict
        """
        logging.info('Converting properties to correct convention.')
        converted_properties = {}
        for key in list(self.properties):
            converted_key = self.convert_string(key, conversion_type)
            converted_properties[converted_key] = self.properties[key]
            if isinstance(self.properties[key], dict):
                converted_subproperties = {}
                for sub_key in list(self.properties[key]):
                    converted_sub_key = self.convert_string(sub_key, conversion_type)
                    converted_subproperties[converted_sub_key] = self.properties[key][sub_key]
                converted_properties[converted_key] = converted_subproperties
        self.properties = converted_properties
        logging.debug(f'Converted Properties: {converted_properties}')
        return converted_properties
