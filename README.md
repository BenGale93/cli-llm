## Introduction

This Python library provides a simple way to create and run custom Large
Language Model (LLM) tools using a command-line interface. It is a Python
re-implementation of [rust-devai](https://github.com/jeremychone/rust-devai),
offering a user-friendly interface for developers to build their own LLM
applications.

## Installation

To utilize this library, you will currently need to clone the repository and
then install it as a [`uv`](https://docs.astral.sh/uv/) tool. Follow these
steps after cloning.

```bash
cd cli-llm
uv tool install .
```

## LLM Set Up

Currently, the tool defaults to `llama3.2:3b` and communicates with it using
the `llm` Python library and the `llm-ollama` plugin. Its documentation can be
found [here](https://github.com/simonw/llm/tree/main?tab=readme-ov-file#llm).

To use the default, you need `ollama` to be installed on your system and
running the `llama3.2:3b` model. Install `ollama` using the instructions
[here](https://github.com/ollama/ollama?tab=readme-ov-file#ollama), start a
server in a shell using `ollama serve`, and then pull the desired model using
`ollama pull llama3.2:3b`.

### Setting API keys

Alternatively, to use an LLM via an API, you will need to set an API key with
the `llm` library, follow their
[instructions](https://github.com/simonw/llm/tree/main?tab=readme-ov-file#getting-started).

## Usage

The library is designed to make it easy to run your own LLM tools. By default
it will search the `$HOME/.local/share/cli-llm` folder (or equivalent on other
platforms), for the tool. Here's an example of how to use the `run` command:

```bash
$ clm run python_file --path tests
```

This will search for `python_file.py`, look for an attribute inside the file
called "tool" which should be an instance of `click.Command`. It will then run
the command with the optional argument "path=tests".

The LLM tool itself should be defined by a `click.command`. For instance:

````python
# readme.py
"""README generation tool.

Example usage:

`clm run readme src/ --pattern "*.py"`
"""

from pathlib import Path

import click

from cli_llm import ClmConfig, helpers, run

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


@click.command()
@click.argument("path", type=Path)
@click.option("--pattern", type=str, default="*")
@click.pass_obj
def tool(config: ClmConfig, path: Path, pattern: str) -> None:
    """Correct the grammar of a given python file."""
    file_contents = helpers.gather_file_contents(search_path=path, pattern=pattern)
    data = {"files": file_contents}

    ai_response = run(config, PROMPT, data)

    ai_response.write_to_file("README.md")

````

Place `readme.py` in `~/.local/share/cli-llm` and you can run it with:

```bash
clm run readme src/ --pattern "*.py"
```

It will save a new README file in the current working directory, based on the
contents of your library. Experiment with the prompt to fine-tune the result.

## Listing all available tools

To list all tools available, run:

```bash
clm run --help
```

## New Command

To create a skeleton script you can use the `new` command:

```bash
clm new tool-name --dest tools/
```

## Advanced Usage

### Sub-tools

You can place multiple commands inside a single python file by making use of
`click`'s more advanced subcommand feature. As long as the entry point is
`tool` (usually this would be `cli` in a normal `click` project) it will gather
all subcommands.

You can then list all sub-tools by running the below. Where filename is the
name of the Python file containing the sub-tools.

```bash
clm run filename --help
```

For an example of what this would look like, checkout `examples/poetry.py` in
this repo.

### Lookup warning

If you have a Python file in the `tools_dir` that does not have a `tool`
attribute, a warning will be emitted. To turn this off, add `tool = None` to
the Python file.

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
