import configparser
from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str


@dataclass
class Config:
    bot: BotConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)
    print(config)

    return Config(
        bot=BotConfig(**config["bot"]),
    )