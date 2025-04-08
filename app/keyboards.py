from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from app.utils import safe_callback_data

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Быстрый поиск'), KeyboardButton(text='Поиск статей')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите способ поиска"
)


def get_article_buttons(titles: list[str]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=title, callback_data=f"wiki:{safe_callback_data(title)}")]
        for title in titles
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)