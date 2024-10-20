"""Configuration for CLI-LLM."""

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

DIRS = PlatformDirs("cli-llm", "BAG")


class ClmConfig(BaseSettings):
    """Config class for the application."""

    ll_model: str = Field(default="llama3.2:latest")
    tools_dir: Path = Field(default=DIRS.user_data_path)

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "cli-llm"),
        toml_file=DIRS.user_config_path / "cli_llm.toml",
    )

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

    def tool_files(self) -> list[Path]:
        """List of all the files that might contain an LLM tool."""
        tool_files = list(self.tools_dir.rglob("*.py"))
        tool_files.sort()
        return tool_files
