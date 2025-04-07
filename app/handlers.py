from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import app.keyboards as kb
import asyncio
import wikipedia

router = Router()
SEARCH_TYPES = ("Quick", "Select")
search = SEARCH_TYPES[0]


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
    await message.answer('ℹ️ Напиши любое слово, и я поищу статью на Википедии.')


# F (magic filter) handler
@router.message(F.text == 'Быстрый поиск')
async def quick_search(message: Message):
    global search
    search = SEARCH_TYPES[0]
    await message.answer('✅ Тип поиска выбран: Быстрый поиск')


@router.message(F.text == 'Поиск статей')
async def select_search(message: Message):
    global search
    search = SEARCH_TYPES[1]
    await message.answer('✅ Тип поиска выбран: Поиск статей')


@router.message(F.text)
async def wiki_answer(message: Message):
    try:
        if search == SEARCH_TYPES[1]:
            # Maqola sarlavhalarini qidiradi
            result_list = await asyncio.to_thread(wikipedia.search, message.text)
            if result_list:
                result = "\n".join([f"• {item}" for item in result_list])
            else:
                result = "😕 Ничего не найдено."
        else:
            # To'liq maqola
            result = await asyncio.to_thread(wikipedia.summary, message.text)
        await message.answer(result)
    except Exception as e:
        await message.answer(f"❌ Ошибка при поиске: {e}")



# Photo handler
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"🖼️ Фото получено! ID: {message.photo[-1].file_id}")