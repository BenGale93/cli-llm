# README

## Introduction

This Python library provides a simple way to create and run custom Large
Language Model (LLM) tools using a CLI interface. It is a Python
re-implementation of [rust-devai](https://github.com/jeremychone/rust-devai)

## Installation

To use this library, you will currently need to clone the repo and then install
it as a `uv` tool:

```bash
cd cli-llm
uv tool install .
```

## Usage

The library is designed to make it easy to run your own tools. Here's an
example of how to use the `run` command:

```bash
$ clm run python_file:ToolClass -p parameter1=value1 -p parameter2=value2
```

This will run the specified LLM tool with the given parameters.

The LLM tool itself should be defined in a python file and contain a class that
inherits from `cli_llm.ToolRunnerInterface`. For example:

````python
# readme.py
"""README generation tool."""

import contextlib
from pathlib import Path
from typing import Any

import llm

from cli_llm.run import ToolRunnerInterface

TEST_PROMPT = """
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

    prompt = TEST_PROMPT

    def gather_data(self, **kwargs: Any) -> dict[str, Any]:
        """Gather the source tree."""
        search_path = kwargs.get("path", Path.cwd())
        pattern = kwargs.get("pattern", "*")
        files = list(Path(search_path).rglob(pattern))
        file_contents = []
        for f in files:
            if not f.is_file():
                continue
            with contextlib.suppress(UnicodeDecodeError):
                contents = f.read_text()
                file_contents.append((f, contents))
        return {"files": file_contents}

    def process(self, ai_response: llm.Response, _data: dict[str, Any]) -> None:
        """Save the new README."""
        Path("README.md").write_text(ai_response.text())

````

Assuming this file is in your working directory, you can run it with:

```bash
clm run readme:Readme -p path=src/ -p "pattern=*.py"
```

It will then save a new README file in the current working directory, based on
the contents of your library. Play with prompt to fine-tune the result.

# Plans

- Add ability to place and find tools in the `.local` directory. Making them
    useful across projects.
- Extract common functions into the `helper` module.
- Add config support.
