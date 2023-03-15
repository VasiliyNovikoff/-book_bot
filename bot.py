import asyncio
import logging
from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from keyboards.main_menu import set_main_menu
from handlers import user_handlers, other_handlers


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурирование и запуск логирования
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о запуске бота
    logger.info('Бот запущен!')

    # Загружаем config в переменную config
    config: Config = load_config()

    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token,
                   parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    # Настраиваем главное меню бота
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        # Запускаем бот
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        #  Выводим сообщение об ошибке в консоль,
        #  если получены исключения KeyboardInterrupt или SystemExit
        logger.error('Бот остановлен!')
