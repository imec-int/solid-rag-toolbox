from typing import Tuple, Type
from pydantic_settings import (
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)
from .config import Application
import logging


class Settings(Application):
    model_config = SettingsConfigDict(yaml_file="config.yaml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[Application],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)

    def setup_logging(self):
        logging.basicConfig(level=self.logLevel.value)
        logger = logging.getLogger(__name__)
        logger.info(f"Starting up with config: {self.model_dump()}")
