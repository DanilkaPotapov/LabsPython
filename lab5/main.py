import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '8423151403:AAGJfBmVkqZ-nucGd5D5KtFZpR1KtlK5hZ0'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="ℹ️ Информация"), KeyboardButton(text="🖼 Фото")],
            [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я простой бот с кнопками.\nВыберите действие:",
        reply_markup=get_main_keyboard()
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n/start - Начать работу\n/help - Помощь\n\nИспользуйте кнопки для взаимодействия!",
        reply_markup=get_main_keyboard()
    )

@dp.message()
async def handle_buttons(message: types.Message):
    if message.text == "ℹ️ Информация":
        await message.answer("Это простой демонстрационный бот на aiogram с кнопками.")
    
    elif message.text == "🖼 Фото":
        await message.answer_photo(
            photo="https://pixabay.com/illustrations/info-information-tips-icon-support-553635/",
            caption="Вот пример фотографии!"
        )
    
    elif message.text == "📞 Контакты":
        await message.answer("Контакты:\nEmail: example@mail.com\nТелефон: +7 (XXX) XXX-XX-XX")
    
    elif message.text == "⚙️ Настройки":
        await message.answer("Раздел настроек. Здесь можно добавить функционал.")
    
    else:
        await message.answer(
            "Я не понимаю эту команду. Используйте кнопки или /help",
            reply_markup=get_main_keyboard()
        )

async def main():
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
