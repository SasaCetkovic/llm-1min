import llm
import requests
from pydantic import Field, field_validator
from typing import Optional, List

@llm.hookimpl
def register_models(register):
    # Register available 1minai models
    models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
        "o1-preview",
        "o1-mini",
        "o3-mini",
        "mistral-large-latest",
        "mistral-small-latest",
        "mistral-nemo",
        "pixtral-12b",
        "claude-3-opus-20240229",
        "claude-3-7-sonnet-20250219",
        "claude-3-5-sonnet-20240620",
        "claude-3-5-haiku-20241022",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "deepseek-chat",
        "deepseek-reasoner",
        "grok-2",
        "command",
        "sonar",
        "sonar-pro",
        "sonar-reasoning",
        "sonar-reasoning-pro",
        "meta/meta-llama-3.1-405b-instruct",
        "meta/meta-llama-3-70b-instruct",
        "meta/llama-2-70b-chat"
    ]
    for model_id in models:
        register(OneMin(model_id))

class OneMinOptions(llm.Options):
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate",
        default=None,
    )

    temperature: Optional[float] = Field(
        description="Controls randomness in the response. Higher values mean more random completions",
        default=1.0,
    )

    stream: Optional[bool] = Field(
        description="Whether to stream the response",
        default=False,
    )

    web_search: Optional[bool] = Field(
        description="Whether to enable web search for responses",
        default=False,
    )

    num_of_sites: Optional[int] = Field(
        description="Number of sites to search when web_search is enabled",
        default=1,
    )

    max_word: Optional[int] = Field(
        description="Maximum number of words when web_search is enabled",
        default=500,
    )

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, temperature):
        if not (0.0 <= temperature <= 2.0):
            raise ValueError("temperature must be between 0 and 2")
        return temperature

class OneMin(llm.Model):
    needs_key = "1minai"
    key_env_var = "ONEMINAI_API_KEY"
    can_stream = True
    base_url = "https://api.1min.ai/api/features"

    class Options(OneMinOptions): ...

    def __init__(self, model_id):
        self.clean_model_id = model_id
        self.model_id = "1min/" + model_id

    def execute(self, prompt, stream, response, conversation):
        api_key = self.get_key()
        headers = {
            "API-KEY": api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "type": "CHAT_WITH_AI",
            "model": self.clean_model_id,
            "promptObject": {
                "prompt": prompt.prompt,
                "isMixed": False,
                "webSearch": prompt.options.web_search,
                "numOfSite": prompt.options.num_of_sites,
                "maxWord": prompt.options.max_word
            }
        }

        if stream:
            try:
                response = requests.post(
                    f"{self.base_url}?isStreaming=true",
                    json=payload,
                    headers=headers,
                    stream=True
                )
                response.raise_for_status()

                buffer = b""

                for chunk in response.iter_content(chunk_size=2):
                    if chunk:
                        buffer += chunk

                        try:
                            decoded = buffer.decode('utf-8')
                            yield decoded
                            # Reset buffer after successful decode
                            buffer = b""
                        except UnicodeDecodeError:
                            # If we can't decode yet, we might have a partial character
                            # Continue collecting bytes until we can decode
                            pass

                # Handle any remaining bytes in buffer
                if buffer:
                    yield buffer.decode('utf-8', errors='ignore')

            except Exception as e:
                raise llm.ModelError(f"API request failed: {str(e)}")

        else:
            try:
                response = requests.post(self.base_url, json=payload, headers=headers)
                response.raise_for_status()
                result = response.json()

                content = result['aiRecord']['aiRecordDetail']['resultObject'][0]

                yield content

            except KeyError:
                raise llm.ModelError("Malformed API response")
            except Exception as e:
                raise llm.ModelError(f"API request failed: {str(e)}")

    def __str__(self):
        return f"1minAI: {self.model_id}"
