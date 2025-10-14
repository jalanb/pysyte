# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Module Overview

The `pysyte.ai` module provides AI and language model integration functionality for Python applications. It is part of the larger pysyte project, a foundational Python library that "adds batteries to Python, bash, and other languages near them".

## Architecture

The module is organized into AI service integration components:

### Core Components

- **`apis.py`**: Base API provider classes and configuration framework for AI services
- **`open_ai.py`**: OpenAI integration with chat completion and model selection
- **`__main__.py`**: Example CLI application demonstrating OpenAI usage with interactive chat
- **`open_ai.toml`**: Configuration file for OpenAI API settings and models

### Key Design Patterns

- **Configuration-Driven**: Uses `pysyte.config.types.ModuleConfiguration` for managing API keys and settings
- **Interactive CLI**: Example application with Rich printing and user input for chat interactions
- **Model Abstraction**: Namespace-based model selection (davinci, curie, babbage, ada)
- **Conversation Management**: Message history handling for multi-turn conversations

## Development Commands

All commands should be run from the project root (`/opt/clones/github/jalanb/pysyse/__dev__/`):

```bash
# Code formatting
tox -e formats    # Apply black (-S for single quotes) and isort formatting

# Linting and type checking
tox -e lints      # Run black, blackdoc, isort, flake8, mypy

# Testing
tox -e devs       # Fast development tests (--exitfirst, skip slow tests)
tox -e tests      # Full test suite with coverage
tox -e pudb       # Run tests with pudb debugger

# Run the AI module directly
python -m pysyte.ai "What is the meaning of life?"
```

## Key APIs

### OpenAI Integration
```python
from pysyte.ai.open_ai import OpenaiApp

# Initialize with key provider
app = OpenaiApp("wwts")

# Send messages to chat completion
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello!"}
]
choices = app.ask(messages)
```

### Configuration
```python
from pysyte.ai.apis import ApiConfiguration, Apis

# Set up API configuration
api = Apis(name="openai")
config = ApiConfiguration(file="config.toml", key="api_key", api=api)
```

## Configuration Files

- **`open_ai.toml`**: Contains model settings, token limits, and API configuration
- Expects API keys to be managed through pysyte's configuration system
- Uses namespace-based model selection for different use cases

## Integration Context

This ai module integrates with:
- **`pysyte.config`**: Configuration management and API key handling
- **`pysyte.cli.exits`**: Exit code management for CLI applications
- **`pysyte.oss.getch`**: User input utilities for interactive prompts
- **`pysyte.types.dictionaries`**: NameSpaces for structured data handling

## Development Notes

- The module expects OpenAI API keys to be configured through pysyte's config system
- Interactive examples use Rich for enhanced terminal output
- Model selection follows OpenAI's naming conventions (text-davinci-003, etc.)
- Conversation management supports multi-turn chat interactions
- Error handling and exit codes follow pysyte conventions