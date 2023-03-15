from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command, Text
from aiogram import Router
from database.database import users_dp, user_dict_template
from copy import deepcopy
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_pagination_keyboard
from services.file_hadling import book

router: Router = Router()


# Этот хэндлер будет срабатывать на коммунды /start,
# добавлять пользователя в базы данных, если его там еще не было
# и отправлять ему преветственное сообщение
@router.message(CommandStart())
async def process_command_start(message: Message):
    if message.from_user.id not in users_dp:
        users_dp[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(text=LEXICON['/start'])


# Этот хэндлер будет срабатывать на команды /help
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'])


# Этот хэндлер будет обрабатывать команду /beginning
# и отправлять пользователю первую страницу книгу с кнопками пагинации
@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    users_dp[message.from_user.id]['page'] = 1
    text = book[users_dp[message.from_user.id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_keyboard(
                             'backward',
                             f'{users_dp[message.from_user.id]["page"]} / {len(book)}',
                             'forward'))


# Этот хэндлер будет срабатывать на команду /continue
# и отправлять пользователю страницу книги, на которой он остановился
# в процессе взаимодействия с ботом
@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    text = book[users_dp[message.from_user.id]['page']]
    await message.answer(text=text,
                         reply_markup=create_pagination_keyboard(
                             'backward',
                             f'{users_dp[message.from_user.id]["page"]} / {len(book)}',
                             'forward'))









