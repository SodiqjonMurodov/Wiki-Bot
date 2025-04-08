from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import app.keyboards as kb
import asyncio
import wikipedia
from app.keyboards import get_article_buttons

router = Router()
SEARCH_TYPES = ("Quick", "Select")
search = SEARCH_TYPES[0]
search_cache = {}  # Foydalanuvchi ID -> maqolalar ro'yxati
user_languages = {}  # Foydalanuvchi ID -> Til


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
    global search_cache

    try:
        if search == SEARCH_TYPES[1]:
            # Foydalanuvchi izlagan maqolalar sarlavhalarini olish
            result_list = await asyncio.to_thread(wikipedia.search, message.text, results=10)
            
            if result_list:
                # Keshga saqlaymiz foydalanuvchi bo‘yicha
                search_cache[message.from_user.id] = result_list

                # Tugmalar uchun sarlavhalarni qisqartirish
                max_title_length = 50  # Tugma nomi maksimal uzunligi
                short_titles = [title[:max_title_length] + "..." if len(title) > max_title_length else title for title in result_list]

                markup = get_article_buttons(short_titles)

                await message.answer("🔎 Найденные статьи:", reply_markup=markup)
            else:
                await message.answer("😕 Ничего не найдено.")
        else:
            # To‘liq maqola chiqarish
            result = await asyncio.to_thread(wikipedia.summary, message.text)

            # Agar maqola uzun bo'lsa, uni qismlarga bo'lamiz
            max_length = 4096  # Telegramning maksimal uzunligi
            while len(result) > max_length:
                await message.answer(result[:max_length])  # Birinchi qismni yuboramiz
                result = result[max_length:]  # Qolgan qismini keyin yuboramiz


            await message.answer(result)
    except Exception as e:
        await message.answer(f"❌ Ошибка при поиске: {e}")


@router.callback_query(F.data.startswith("wiki:"))
async def show_article(callback: CallbackQuery):
    title = callback.data.split("wiki:")[1]

    try:
        summary = await asyncio.to_thread(wikipedia.summary, title)

        chunks = [summary[i:i + 4000] for i in range(0, len(summary), 4000)]

        await callback.message.answer(f"<b>{title}</b>", parse_mode='HTML')
        for chunk in chunks:
            await callback.message.answer(chunk)

    except Exception as e:
        await callback.message.answer(f"❌ Не удалось получить статью: {e}")


# Photo handler
@router.message(F.photo)
async def get_photo(message: Message):
    await message.answer(f"🖼️ Фото получено! ID: {message.photo[-1].file_id}")