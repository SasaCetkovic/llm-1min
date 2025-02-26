# llm-1min

[![PyPI](https://img.shields.io/pypi/v/llm-mistral.svg)](https://pypi.org/project/llm-1min/)
[![Changelog](https://img.shields.io/github/v/release/SasaCetkovic/llm-1min?include_prereleases&label=changelog)](https://github.com/SasaCetkovic/llm-1min/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/SasaCetkovic/llm-1min/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin providing access to [1minAI](https://app.1min.ai) models using their [API](https://api.1min.ai/api)

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).

```zsh
llm install llm-1min
```

## Usage

First, set an [API key](https://app.1min.ai/api) for 1minAI:

```zsh
llm keys set 1minai
# Paste the key here
```

You can also set the API key by assigning it to the environment variable ONEMINAI_API_KEY.

Run `llm models` to list the models, and `llm models --options` to include a list of their options.

Run `llm models default 1min/gpt-4o` to set gpt-4o as the default model.

Run prompts like this:

```zsh
llm -m 1min/gtp-4o "How many push-ups can Chuck Norris do?"
llm -m 1min/o3-mini "How much wood would a woodchuck chuck if the woodchuck would chuck Chuck Norris?"
llm -m 1min/claude-3-5-haiku-20241022 "What's the meaning of life?"
```

### Currently supported models

- 1min/gpt-4o
- 1min/gpt-4o-mini
- 1min/gpt-4-turbo
- 1min/gpt-4
- 1min/gpt-3.5-turbo
- 1min/o1-preview
- 1min/o1-mini
- 1min/o3-mini
- 1min/mistral-large-latest
- 1min/mistral-small-latest
- 1min/mistral-nemo
- 1min/claude-3-opus-20240229
- 1min/claude-3-5-sonnet-20240620
- 1min/claude-3-5-haiku-20241022
- 1min/gemini-1.5-pro
- 1min/gemini-1.5-flash
- 1min/deepseek-chat
- 1min/grok-2
- 1min/command
- 1min/meta/meta-llama-3.1-405b-instruct

## To Do

- [ ] Add support for conversations
- [ ] Add support for other 1minAI _features_ (e.g. code, content, image, and audio generation, translation, content transformation, etc.)
- [ ] Improve error handling

### Caveats

[1minAI API](https://gleaming-wren-2af.notion.site/1min-AI-API-Docs-111af080bd8f8046a4e6e1053c95e047) is not similar to any other LLM provider. It does not support message arrays with different roles. Conversations must be started with a separate API call. Therefore, the llm chat command will probably not be supported, and the conversation feature will be implemented as a separate command.

## Contributing

Contributions are welcome, feel free to submit a PR.

This plugin was made after the [llm-anthropic](https://github.com/simonw/llm-anthropic) and other plugins by Simon Willison.
