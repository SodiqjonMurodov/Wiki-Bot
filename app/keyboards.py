from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Быстрый поиск'), KeyboardButton(text='Поиск статей')]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите способ поиска"
)