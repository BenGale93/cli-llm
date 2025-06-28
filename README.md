## Introduction

This library simplifies creating and running custom Large Language Model (LLM)
tools from your command line. It's a Python re-implementation of the excellent
[rust-devai](https://github.com/jeremychone/rust-devai), providing a
user-friendly interface for building your own LLM-powered applications.

## Installation

To get started, clone the repository and install it as a
[`uv`](https://docs.astral.sh/uv/) tool. After cloning the repository, run the
following commands:

```bash
cd cli-llm
uv tool install .
```

## LLM Setup

By default, this tool uses `llama3.2:3b` and communicates with it via the `llm`
Python library and its `llm-ollama` plugin. You can find the `llm`
documentation
[here](https://github.com/simonw/llm/tree/main?tab=readme-ov-file#llm).

To use the default model, you'll need `ollama` installed and running.
1. Install `ollama` using the instructions [here](https://github.com/ollama/ollama).
2. Start the Ollama server in a new terminal: `ollama serve`.
3. Pull the required model: `ollama pull llama3.2:3b`.

### Using API Keys

Alternatively, to use an LLM provider's API, you must set an API key. Follow
the `llm` library's
[instructions](https://github.com/simonw/llm/tree/main?tab=readme-ov-file#getting-started)
to configure your keys.

## Usage

This library makes it easy to execute your custom LLM tools. By default, it
searches for tools in the `$HOME/.local/share/cli-llm` folder (or the
equivalent on other platforms).

Here's an example of how to use the `run` command:

```bash
$ clm run python_file --path tests
```

This command searches for `python_file.py` in your tools directory. Inside that
file, it looks for a `tool` attribute, which must be a `click.Command`
instance. It then executes the command, passing along any additional arguments
like `--path tests`.

The LLM tool itself must be defined as a `click.Command`. For example:

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
- Below are some {{lang}} files from a library.
- Each file will be listed with its name and then its content.
- Write a README in markdown format that explains how to use the {{lang}} library.

{% for f, contents in files %}
Filename: {{f}}

```{{lang}}
{{contents}}
```
{% endfor %}
"""


@click.command()
@click.argument("path", type=Path)
@click.option("-l", "--lang", type=str, default="")
@click.option("-p", "--pattern", type=str, default="*")
@click.option("-o", "--output", type=Path, default=Path("README.md"))
@click.pass_obj
def tool(config: ClmConfig, path: Path, lang: str, pattern: str, output: Path) -> None:
    """Write a README for a given library."""
    file_contents = helpers.gather_file_contents(search_path=path, pattern=pattern)
    data = {"files": file_contents, "lang": lang}

    ai_response = run(config, PROMPT, data)

    ai_response.write_to_file(output)

````

Place this `readme.py` file in `~/.local/share/cli-llm`, and you can run it with:

```bash
clm run readme src/ --pattern "*.py"
```

This will generate a new `README.md` in your current directory based on the
contents of your library. Experiment with the prompt to fine-tune the results!

## Listing Available Tools

To see a list of all available tools, run:

```bash
clm run --help
```

## Creating a New Tool

You can create a skeleton for a new tool using the `new` command:

```bash
clm new tool-name --dest tools/
```

## Advanced Usage

### Sub-tools

You can bundle multiple commands into a single Python file using `click`'s
subcommand feature. As long as the primary entry point is named `tool` (this
would typically be `cli` in a standard `click` project), the library will
automatically discover all its subcommands.

To list the sub-tools within a specific file, run the following command, where
`filename` is the name of your Python file:

```bash
clm run filename --help
```

For a practical example, see `examples/poetry.py` in this repository.

### Suppressing Lookup Warnings

If a Python file in your `tools_dir` does not have a `tool` attribute, the
library will emit a warning. To suppress this for a specific file, simply add
`tool = None` to it.

## Configuration

Configuration is flexible: you can use CLI options, environment variables,
a dedicated config file, or your project's `pyproject.toml`.

The dedicated config file is located at `~/.config/cli-llm/cli_llm.toml` on
Unix-like systems and in equivalent locations on other platforms.

### `ll_model`

Specifies the LLM model to use.

- **Default**: `"llama3.2:3b"`
- **Type**: `str`

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

### `tools_dir`

The directory or directories to search for tools.

- **Default**: `~/.local/share/cli-llm`
- **Type**: `Path | list[Path]`

Examples:

```toml
# pyproject.toml
[tool.cli-llm]
tools_dir = "~/tools"
```

```toml
# cli_llm.toml
tools_dir = ["~/tools", "~/.local/share/cli-llm"]
```
