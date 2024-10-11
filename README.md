## Introduction

This Python library provides a simple way to create and run custom Large
Language Model (LLM) tools using a command-line interface. It is a Python
re-implementation of [rust-devai](https://github.com/jeremychone/rust-devai),
offering a user-friendly interface for developers to build their own LLM
applications.

## Installation

To utilize this library, you will currently need to clone the repository and
then install it as a [`uv`](https://docs.astral.sh/uv/) tool. Follow these
steps:

```bash
cd cli-llm
uv tool install .
```

## LLM Set Up

Currently, the tool defaults to `llama3.2:3b` and communicates with it using
the `llm` Python library and the `llm-ollama` plugin. Therefore, it requires
`ollama` to be installed on your system running the `llama3.2:3b` model.
Install `ollama`, start a server in a shell using `ollama serve`, and then pull
the desired model using `ollama pull llama3.2:3b`.

## Usage

The library is designed to make it easy to run your own LLM tools. Here's an
example of how to use the `run` command:

```bash
$ clm run python_file:ToolClass -p parameter1=value1 -p parameter2=value2
```

This will execute the specified LLM tool with the given parameters.

The LLM tool itself should be defined in a Python file and contain a class that
inherits from `cli_llm.ToolRunnerInterface`. For instance:

````python
# readme.py
"""README generation tool.

Example usage:

`clm run readme:Readme -p path=src/ -p "patten=*.py"`
"""

from pathlib import Path
from typing import Any

import llm

from cli_llm import ToolRunnerInterface, helpers

# The template should use Jinja2 syntax to construct the prompt.
PROMPT = """
- Below are some python files from a library.
- Each file will be listed with its name and then its content.
- Write a README in markdown format that explains how to use the python library.

{% for f, contents in files %}
Filename: {{file}}

```python
{{contents}}
```
{% endfor %}
"""


class Readme(ToolRunnerInterface):
    """Generate a README for the library."""

    prompt = PROMPT

    def gather_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gather the source tree."""
        search_path = kwargs.get("path", Path.cwd())
        pattern = kwargs.get("pattern", "*")
        file_contents = helpers.gather_file_contents(search_path=search_path, pattern=pattern)
        return {"files": file_contents} # the keys in this dictionary are used in the prompt template

    # The `data` dictionary is the same as the dictionary returned from the gather_data method above
    def process(self, ai_response: llm.Response, data: dict[str, Any]) -> None:
        """Save the new README."""
        Path("README.md").write_text(ai_response.text())

````

Assuming this file is in your working directory, you can run it with:

```bash
clm run readme:Readme -p path=src/ -p "pattern=*.py"
```

It will then save a new README file in the current working directory, based on
the contents of your library. Experiment with the prompt to fine-tune the
result.

## Plans

- Add functionality to place and find tools in the `.local` directory, making them useful across projects.
- Extract common functions into the `helper` module.
- Implement configuration support, so API keys (e.g., for authentication) can be specified.
