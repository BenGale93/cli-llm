"""Improve the writing of a given file.

Example usage:

`clm run improve:Improve -p path=FILE.txt`
"""

from pathlib import Path

from cli_llm import Response, StringDict, ToolRunnerInterface

PROMPT = """
- The user will provide you with the content of a file.
- You will improve the writing style to be more grammatically correct and engaging.
- Do not respond with anything than the modified file.

```
{{file.read_text()}}
```
"""


class Improve(ToolRunnerInterface):
    """Improve the writing of a given file."""

    prompt = PROMPT

    def gather_data(self, cli_kwargs: StringDict) -> StringDict:
        """Gather the file to improve."""
        filename = Path(cli_kwargs["path"])
        return {"file": filename}

    def process(self, ai_response: Response, data: StringDict) -> None:
        """Save the AI response to the given file."""
        filename = Path(data["file"])
        contents = ai_response.text()

        if not contents.endswith("\n"):
            contents += "\n"

        filename.write_text(contents)
