from dataclasses import dataclass

import openai

from pysyte.config.types import ModuleConfiguration


@dataclass
class Apis:
    """A provider of APIs"""

    name: str = "Fred"


@dataclass
class ApiConfiguration(ModuleConfiguration):
    api: Apis

    def __init__(self, file: str, key: str, api: Apis):
        super().__init__(file)
        openai.api_key = self.keys[key][api.name]
