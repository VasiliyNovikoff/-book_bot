from dataclasses import dataclass

from environs import Env


@dataclass
class TgBot:
    token: str               # Токен для доступа к вашему боту
    admins_id: list[int]      # Список id админов бота


@dataclass
class Config:
    tg_bot: TgBot


# Функция, которая будет читать наш .env и возвращать
# экземпляр класса Config с заполненными полями token и admins_id
def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               admins_id=list(map(int, env.list('ADMINS_ID')))))
