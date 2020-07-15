import errors
import jmespath
import json
from enum import auto, Enum
from typing import Any


class JsonQueryHandler:
    class JsonQueryLanguage(Enum):
        JMESPATH = auto()

    def __init__(self, language: str):
        if not self.__class__.accepts(language):
            raise errors.generic.unsupported_value_for_variable(variable="language", value=language)
        self.language = self.JsonQueryLanguage[language.upper()]

    @classmethod
    def accepts(cls, language: str) -> bool:
        return language.upper() in cls.JsonQueryLanguage.__members__

    def execute(self, query: str, o: Any):
        if self.language == self.JsonQueryLanguage.JMESPATH:
            result = jmespath.search(query, o)
        else:
            raise errors.generic.unsupported_option_for_function(
                function="JsonQueryHandler.execute",
                option_name="language", option_value=self.language.name
            )
        return result


def parse_json_file(path: str):
    with open(path, "r") as f:
        content = json.load(f)
    return content
