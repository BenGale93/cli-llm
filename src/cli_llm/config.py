"""Configuration for CLI-LLM."""

from pathlib import Path

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

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "cli-llm"),
        toml_file=Path(DIRS.user_config_dir) / "cli_llm.toml",
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
