from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart, Command, Text
from aiogram import Router
from database.database import users_dp, user_dict_template
from copy import deepcopy
from lexicon.lexicon import LEXICON
from keyboards.pagination_kb import create_pagination_keyboard
from services.file_hadling import book
from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_bookmarks
from filters.filters import IsDigitCallbackData, IsDelBookmarkCallbackData

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
                             f'{users_dp[message.from_user.id]["page"]}/{len(book)}',
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
                             f'{users_dp[message.from_user.id]["page"]}/{len(book)}',
                             'forward'))


# Этот хэндлер будет срабатывать на команду /bookmarks
# и отправлять пользователю список закладок, если они есть
@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    if users_dp[message.from_user.id]['bookmarks']:  # type: ignore
        await message.answer(text=LEXICON[message.text],
                             reply_markup=create_bookmarks_keyboard(
                                 *users_dp[message.from_user.id]['bookmarks']))

    else:
        await message.answer(text=LEXICON['no_bookmarks'])


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
# во время взаимодействия пользователя с книгой-ботом
@router.callback_query(Text(text='forward'))
async def process_forward_press(callback: CallbackQuery):
    if users_dp[callback.from_user.id]['page'] < len(book):
        users_dp[callback.from_user.id]['page'] += 1
        text = book[users_dp[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_dp[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
# во время взаимодействия пользователя с книгой-ботом
@router.callback_query(Text(text='backward'))
async def process_backward_press(callback: CallbackQuery):
    if users_dp[callback.from_user.id]['page'] > 1:
        users_dp[callback.from_user.id]['page'] -= 1
        text = book[users_dp[callback.from_user.id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_dp[callback.from_user.id]["page"]}/{len(book)}',
                'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с номером текущей страницы и добавлять текущую страницу в закладки
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def process_page_press(callback: CallbackQuery):
    users_dp[callback.from_user.id]['bookmarks'].add(
        users_dp[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки!')


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок
@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_dp[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_keyboard(
                                         'backward',
                                         f'{users_dp[callback.from_user.id]["page"]/len(book)}',
                                         'forward'))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# редактировать под списом закладок
@router.callback_query(Text(text='edit_bookmarks'))
async def process_edit_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['edit_bookmarks'],
                                     reply_markup=create_edit_bookmarks(
                                         *users_dp[callback.from_user.id]['bookmarks']))
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие кнопки отменить
# во время работы со списком закладок (просмотр и редактирование)
@router.callback_query(Text(text='cancel'))
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])
    await callback.answer()


# Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
# с закладкой из списка закладок к удалению
@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    users_dp[callback.from_user.id]['bookmarks'].remove(
        int(callback.data[:-3]))
    if users_dp[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['/bookmarks'],
                                         reply_markup=create_bookmarks_keyboard(
                                             *users_dp[callback.from_user.id]['bookmarks']))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()
