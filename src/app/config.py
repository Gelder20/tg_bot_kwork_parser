import configparser
from dataclasses import dataclass




@dataclass
class BotConfig:
    token: str


@dataclass
class DbConfig:
    user: str
    password: str
    database: str
    host: str


@dataclass
class Config:
    bot: BotConfig
    db: DbConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    return Config(
        bot=BotConfig(**config["bot"]),
        db=DbConfig(**config["database"]),
    )


if __name__=='__main__':
    config = load_config('config.ini')

    from pprint import pprint
    pprint(config)