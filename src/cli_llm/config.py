"""Configuration for CLI-LLM."""

import typing as t
from pathlib import Path

import llm
from platformdirs import PlatformDirs
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    PyprojectTomlConfigSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from cli_llm._logging import ClmLogger

log = ClmLogger()

DIRS = PlatformDirs("cli-llm", "BAG")


class ClmConfig(BaseSettings):
    """Config class for the application."""

    ll_model: str = Field(default="llama3.2:latest", frozen=True)
    tools_dir: Path | list[Path] = Field(default=DIRS.user_data_path, frozen=True)

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "cli-llm"),
        toml_file=DIRS.user_config_path / "cli_llm.toml",
    )

    def model_post_init(self, __context: t.Any) -> None:
        """Initialise the map of potential tool files.

        Currently does not handle name collisions and just overwrites existing tool files.
        """
        tool_files: dict[str, Path] = {}
        tools_dir = [self.tools_dir] if isinstance(self.tools_dir, Path) else self.tools_dir
        for directory in tools_dir:
            dir_ = directory.expanduser().absolute()
            log.info("Looking for tools in: %s", dir_)
            files = {f.stem: f for f in dir_.rglob("*.py")}
            log.info("Found the following tool files %s", files)
            tool_files |= files

        self._tool_files = dict(sorted(tool_files.items()))

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Custom configuration loading priority."""
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            TomlConfigSettingsSource(settings_cls),
            PyprojectTomlConfigSettingsSource(settings_cls),
        )

    def model(self) -> llm.Model:
        """The actual LLM Model."""
        return llm.get_model(self.ll_model)

    @property
    def tool_files(self) -> dict[str, Path]:
        """Map of tools to their script locations."""
        return self._tool_files
