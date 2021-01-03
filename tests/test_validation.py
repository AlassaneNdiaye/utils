import logging
import unittest
from utils.validation import validate

logger = logging.getLogger(__name__)


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.variables = {
            'int': 0,
            'string': 'string value',
            'group.1.1': 0,
            'group.1.2': 0,
            'group.1.3': 0,
            'group.2.1': None,
            'group.2.2': 0,
            'group.3.1': None,
            'group.3.2': None,
            'group.3.3': None
        }

    def tearDown(self):
        del self.variables

    def test_incompatible_mapping(self):
        incompatible_mapping = [
            [['"group.1.1"', '"group.1.2"', '"group.1.3"'], ['"group.2.1"', '"group.2.2"']]
        ]
        self.assertFalse(validate(self.variables, incompatible_mapping=incompatible_mapping)['passed'])

        incompatible_mapping = [
            [['"group.1.1"', '"group.1.2"', '"group.1.3"'], ['"group.3.1"', '"group.3.2"', '"group.3.3"']]
        ]
        self.assertTrue(validate(self.variables, incompatible_mapping=incompatible_mapping)['passed'])

        incompatible_mapping = [
            [['"group.2.1"', '"group.2.2"'], ['"group.3.1"', '"group.3.2"', '"group.3.3"']]
        ]
        self.assertTrue(validate(self.variables, incompatible_mapping=incompatible_mapping)['passed'])

    def test_mandatory_mapping(self):
        mandatory_mapping = [
            [['"group.1.1"', '"group.1.2"', '"group.1.3"']]
        ]
        self.assertTrue(validate(self.variables, mandatory_mapping=mandatory_mapping)['passed'])

        mandatory_mapping = [
            [['"group.2.1"', '"group.2.2"']]
        ]
        self.assertFalse(validate(self.variables, mandatory_mapping=mandatory_mapping)['passed'])

        mandatory_mapping = [
            [['"group.3.1"', '"group.3.2"', '"group.3.3"']]
        ]
        self.assertFalse(validate(self.variables, mandatory_mapping=mandatory_mapping)['passed'])

        mandatory_mapping = [
            [['"group.1.1"', '"group.1.2"', '"group.1.3"'], ['"group.3.1"', '"group.3.2"', '"group.3.3"']]
        ]
        self.assertTrue(validate(self.variables, mandatory_mapping=mandatory_mapping)['passed'])

        mandatory_mapping = [
            [['"group.2.1"', '"group.2.2"'], ['"group.3.1"', '"group.3.2"', '"group.3.3"']]
        ]
        self.assertFalse(validate(self.variables, mandatory_mapping=mandatory_mapping)['passed'])

    def test_type_mapping(self):
        type_mapping = {'int': 'invalid_type'}
        self.assertRaises(ValueError, validate, self.variables, type_mapping=type_mapping)

    def test_type_mapping_int(self):
        type_mapping = {'int': 'int'}
        self.assertTrue(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'string': 'int'}
        self.assertFalse(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'min_value': -10}}
        self.assertTrue(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'min_value': 10}}
        self.assertFalse(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'max_value': 10}}
        self.assertTrue(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'max_value': -10}}
        self.assertFalse(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'min_value': -10, 'max_value': 10}}
        self.assertTrue(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'min_value': 5, 'max_value': 10}}
        self.assertFalse(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'ranges': [[-10, 10]]}}
        self.assertTrue(validate(self.variables, type_mapping=type_mapping)['passed'])

        type_mapping = {'int': {'type': 'int', 'ranges': [[5, 10]]}}
        self.assertFalse(validate(self.variables, type_mapping=type_mapping)['passed'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    suite = unittest.TestSuite()
    suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestValidation))
    runner = unittest.TextTestRunner(buffer=True, tb_locals=True, verbosity=2)
    runner.run(suite)
