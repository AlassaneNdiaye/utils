import errors
import logging
from typing import Any, MutableMapping, MutableSequence, Union
from utils.generic import debug_decorator
from utils.json import JsonQueryHandler
from utils.validation.validators import IntValidator

logger = logging.getLogger(__name__)

json_query_handler = JsonQueryHandler(language="JMESPATH")

GroupMapping = MutableSequence[MutableSequence[MutableSequence[str]]]
TypeMapping = MutableMapping[str, Union[str, MutableMapping[str, Any]]]


@debug_decorator(logger)
def validate(
        variables: MutableMapping[str, Any], mandatory_mapping: GroupMapping = None,
        incompatible_mapping: GroupMapping = None, type_mapping: TypeMapping = None):
    return_value = {
        'passed': True,
        'incompatible_keys': [],
        'invalid_type_keys': [],
        'missing_keys': []
    }

    if mandatory_mapping is not None:
        return_value['missing_keys'].extend(validate_mandatory_mapping(variables, mandatory_mapping))
    if incompatible_mapping is not None:
        return_value['incompatible_keys'].extend(validate_incompatible_mapping(variables, incompatible_mapping))
    if type_mapping is not None:
        return_value['invalid_type_keys'].extend(validate_type_mapping(variables, type_mapping))

    if return_value['missing_keys'] or return_value['incompatible_keys'] or return_value['invalid_type_keys']:
        return_value['passed'] = False

    return return_value


def validate_incompatible_mapping(variables: MutableMapping[str, Any], incompatible_mapping: GroupMapping):
    failed_validations = []

    for groups in incompatible_mapping:
        active_group_count = 0
        for group in groups:
            for key in group:
                value = json_query_handler.execute(query=key, o=variables)
                if value is not None:
                    active_group_count += 1
                    break
            if active_group_count > 1:
                failed_validations.append(groups)
                break

    return failed_validations


def validate_mandatory_mapping(variables: MutableMapping[str, Any], mandatory_mapping: GroupMapping):
    failed_validations = []

    for groups in mandatory_mapping:
        found_valid_group = False
        for group in groups:
            mandatory_keys_defined = True
            for key in group:
                value = json_query_handler.execute(query=key, o=variables)
                if value is None:
                    mandatory_keys_defined = False
                    break
            if mandatory_keys_defined is True:
                found_valid_group = True
                break
        if found_valid_group is False:
            failed_validations.append(groups)

    return failed_validations


def validate_type_mapping(variables: MutableMapping[str, Any], type_mapping: TypeMapping):
    failed_validations = []

    for key, value_type in type_mapping.items():
        if type(value_type) is str:
            value_type = {'type': value_type}
        value = json_query_handler.execute(query=key, o=variables)
        kwargs = value_type.copy()
        kwargs.pop('type')
        if value_type['type'] == 'int':
            if IntValidator.validate(value, **kwargs) is False:
                failed_validations.append(key)
        else:
            raise errors.generic.unsupported_value_for_variable(variable='type', value=value_type['type'])

    return failed_validations
