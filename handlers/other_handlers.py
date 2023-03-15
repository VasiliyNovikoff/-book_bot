from aiogram import Router
from aiogram.types import Message


router: Router = Router()


# Этот хэндлер будет реагировать на все сообщения не предусмотренные логикой бота
@router.message()
async def send_echo(message: Message):
    await message.answer(text=f'Эхо!, {message.text}')
