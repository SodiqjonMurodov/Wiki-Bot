from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import app.keyboards as kb
import wikipedia

router = Router()


# /start handler
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"""👋 Приветствую, {message.from_user.full_name}!

Меня зовут 🤖 <b>Wiki Bot</b> — я твой персональный гид по 📚 <b>Википедии</b>!

🔍 Просто отправь мне любой запрос — и я найду для тебя подходящую статью!

📌 Внизу ты можешь выбрать <b>тип поиска</b>
Жду твой запрос! 😊
""",
parse_mode='HTML',
reply_markup=kb.main)


# Command handler
@router.message(Command("help"))
async def get_help(message: Message):
    await message.answer('Это команда /help')


# F (magic filter) handler
@router.message(F.text)
async def dialog(message: Message):
    result = wikipedia.summary("Wikipedia")
    await message.answer(f'{result}')


# Photo handler
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"ID photo: {message.photo}")