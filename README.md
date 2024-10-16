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

The library is designed to make it easy to run your own LLM tools. By default
it will search the `$HOME/.local/share/cli-llm` folder (or equivalent on other
platforms), for the tool. Here's an example of how to use the `run` command:

```bash
$ clm run python_file:ToolClass -p parameter1=value1 -p parameter2=value2
```

This will search for `python_file.py` and then execute the ToolClass found
within, with the given parameters.

The LLM tool itself should be defined by a class that inherits from
`cli_llm.ToolRunnerInterface`. For instance:

````python
# readme.py
"""README generation tool.

Example usage:

`clm run readme:Readme -p path=src/ -p "pattern=*.py"`
"""

from pathlib import Path

from cli_llm import Response, StringDict, ToolRunnerInterface, helpers

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

    # `cli_kwargs` are the user provided parameters
    def gather_data(self, cli_kwargs: StringDict) -> StringDict:
        """Gather the source tree."""
        search_path = kwargs.get("path", Path.cwd())
        pattern = kwargs.get("pattern", "*")
        file_contents = helpers.gather_file_contents(search_path=search_path, pattern=pattern)
        return {"files": file_contents} # the keys in this dictionary are used in the prompt template

    # The `data` dictionary is the same as the dictionary returned from the gather_data method above
    def process(self, ai_response: Response, data: StringDict) -> None:
        """Save the new README."""
        ai_response.write_to_file("README.md")

````

Place `readme.py` in `~/.local/share/cli-llm` and you can run it with:

```bash
clm run readme:Readme -p path=src/ -p "pattern=*.py"
```

It will save a new README file in the current working directory, based on the
contents of your library. Experiment with the prompt to fine-tune the result.

## Configuration

You can configure via the CLI, environment variables, an app specific config
file, or via pyproject.toml.

The config file is located at `~/.config/cli-llm/cli_llm.toml` on Unix and
equivalent locations on other platforms.


### ll-model

The model to use.

Default value: "llama3.2:3b"

Type: str

Examples:

```toml
# pyproject.toml
[tool.cli-llm]
ll_model = "other"
```

```toml
# cli_llm.toml
ll_model = "other"
```

### tools-dir

The directory to search for tools within.

Default value: `~/.local/share/cli-llm`

Type: Path

Examples:

```toml
# pyproject.toml
[tool.cli-llm]
tools_dir = "~/tools"
```

```toml
# cli_llm.toml
tools_dir = "~/tools"
```

## Plans

- Extract common functions into the `helper` module.
- Extend configuration support, so API keys (e.g., for authentication) can be specified.
