from aiogram.types import ReplyKeyboardMarkup,\
    KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton

# Start screen buttons
update_price = KeyboardButton('Обновить прайс 📃')
update_margin = KeyboardButton('Обновить наценки 💸')
start_screen_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(update_price, update_margin)
