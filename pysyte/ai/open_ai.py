"""Handle openai for pysyte"""

from dataclasses import dataclass

import openai

from pysyte.ai import apis


@dataclass
class AiAppConfig:
    config: apis.ApiConfiguration

@dataclass
class OpenaiApp:
    key_provider: str

    def __post_init__(self):
        self.config = apis.ApiConfiguration(__file__, self.key_provider, apis.Apis("openai"))

    def ask(self, messages: list[dict]):
        response = openai.ChatCompletion.create(
            messages=messages,
            model=self.config.model,
            n=self.config.times,
            max_tokens=self.config.tokens.max,
        )
        return response.choices


jalanb = OpenaiApp("jalanb")
app = jalanb
app.ask(["Have we started now?"])
