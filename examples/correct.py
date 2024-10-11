"""Correct the grammar of a given python file.

Example usage:

`clm run correct:Correct -p path=FILE.txt`
"""

from pathlib import Path

import llm

from cli_llm import StringDict, ToolRunnerInterface

PROMPT = """
- The user will provide you with the content of a Python programming file.
- You will correct the English in the comments, but leave everything else unchanged.
- Only modify comments if there is a spelling or grammar mistake.
- Make sure not to change the code, except for typos within strings.
- Do not change the code itself, only comments.
- Do not respond with anything than the modified code

```python
{{file.read_text()}}
```
"""


class Correct(ToolRunnerInterface):
    """Correct the grammar of a given python file."""

    prompt = PROMPT

    def gather_data(self, cli_kwargs: StringDict) -> StringDict:
        """Gather the file to correct the grammar for."""
        filename = Path(cli_kwargs["path"])
        return {"file": filename}

    def process(self, ai_response: llm.Response, data: StringDict) -> None:
        """Save the AI response to the given file."""
        filename = Path(data["file"])
        contents = ai_response.text()

        if not contents.endswith("\n"):
            contents += "\n"

        filename.write_text(contents)
