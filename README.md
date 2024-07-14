# Intellisys

Intellisys is a Python library that provides intelligence/AI services for the Lifsys Enterprise.

## Installation

You can install Intellisys using pip:

```
pip install intellisys
```

## Usage

Here's a quick example of how to use Intellisys:

```python
from intellisys import get_completion_api

response = get_completion_api("Hello, how are you?", "gpt-3.5-turbo")
print(response)
```

## Features

- Support for multiple AI models (OpenAI, Anthropic, Google, etc.)
- API key management
- JSON formatting and template rendering
- Asynchronous assistant interactions

## License

This project is licensed under the MIT License - see the LICENSE file for details.
