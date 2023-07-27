"""Handle openai for pysyte"""
from dataclasses import dataclass

import openai

from pysyte.ai import apis


@dataclass
class OpenaiApp:
    key_provider: str

    def __init__(self, key_provider):
        self.config = apis.ApiConfiguration(__file__, key_provider, "openai")

    def ask(self, messages):
        response = openai.ChatCompletion.create(
            messages=messages,
            model=self.config.model,
            n=self.config.times,
            max_tokens=self.config.tokens.max,
        )
        return response.choices


jalanb = OpenaiApp("jalanb")
wwts = OpenaiApp("wwts")

app = wwts
