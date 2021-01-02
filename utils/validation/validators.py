from abc import ABC, abstractmethod
from typing import Sequence


class Validator(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, *args, **kwargs):
        pass


class IntValidator(Validator):
    @classmethod
    def validate(
            cls, value: object, min_value: int = None, max_value: int = None,
            ranges: Sequence[Sequence[int]] = None):
        if type(value) is not int:
            return False
        if min_value is not None and min_value > value:
            return False
        if max_value is not None and max_value < value:
            return False
        if ranges is not None:
            for valid_range in ranges:
                if value not in range(*valid_range):
                    return False
        return True
