import asyncio
import logging

from decouple import config

from aiogram import Bot, Dispatcher, Router, types, F
from googletrans import Translator

from aiogram.filters import Command

bot = Bot(token="6977539871:AAHzRM2c3_td94pVwLfY0ZIVpC1XfcsW17Q")
dp = Dispatcher()

translator = Translator('en')

@dp.message(Command("start"))
async def send_welcome(message: types.Message):

    await message.answer("Привіт! Я бот для перекладу тексту. Просто введи текст, і я перекладу його для тебе.")

@dp.message(Command("setlang"))
async def set_language(message: types.Message):

    try:
        lang_codes = message.text.split()[1:]
        from_lang, to_lang = lang_codes
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        await message.answer(f"Мова перекладу встановлена з {from_lang} на {to_lang}.")
    except (IndexError, ValueError):
        await message.answer("Введіть команду у форматі /setlang код_мови_з код_мови_на, наприклад, /setlang uk en.")

@dp.message()
async def translate_text(message: types.Message):

    try:
        text = message.text
        translation = translator.translate(text)
        await message.answer(f"Оригінал: {text}\nПереклад: {translation}")
    except Exception as e:
        logging.exception(e)
        await message.answer("Виникла помилка під час перекладу. Спробуйте ще раз або встановіть мову перекладу за допомогою /setlang.")


async def main():
    print("Starting bot...")
    print("Bot username: @{}".format((await bot.me())))
    await dp.start_polling(bot)

asyncio.run(main())
