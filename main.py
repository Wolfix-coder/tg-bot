import logging
import sys
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from config import TOKEN  # Токен бота з файлу config.py
from text import help_text, about_text, pay_text, price_text, support_url, type_work_text, bb2

# Логування
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Ініціалізація бота та диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

id = int()
id_order = int()
id_user = int()
subject = str()
type_work = int()
order_details = str()
comment = str()
waiting_for_input = ()


order = {
    "id": id,
    "subject" : subject,
    "type_work" : type_work,
    "order_details" : order_details,
    "comment" : comment, 
    "id_order" : id_order

}

# Функція для створення кнопок
def subject_keyboard():

    buttons = [
        [types.InlineKeyboardButton(text="Біоглогія", callback_data="biology")],
        [types.InlineKeyboardButton(text="Всесвітня історія", callback_data="world_history")],
        [types.InlineKeyboardButton(text="Географія", callback_data="geography")],
        [types.InlineKeyboardButton(text="Іноземна мова", callback_data="eng_language")],
        [types.InlineKeyboardButton(text="Інформатика", callback_data="computer_science")],
        [types.InlineKeyboardButton(text="Історія України", callback_data="ua_hisroty")],
        [types.InlineKeyboardButton(text="Зарубіжна література", callback_data="foreign_literature")],
        [types.InlineKeyboardButton(text="Захист України", callback_data="defense_ua")],
        [types.InlineKeyboardButton(text="Математика", callback_data="maths")],
        [types.InlineKeyboardButton(text="Українська література", callback_data="ua_literature")],
        [types.InlineKeyboardButton(text="Українська мова", callback_data="ua_lenguage")],
        [types.InlineKeyboardButton(text="Хімія", callback_data="chemistry")],
        [types.InlineKeyboardButton(text="Фізика", callback_data="physics")],
        [types.InlineKeyboardButton(text="Фізична культура", callback_data="physical_culture")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

def type_work_keyboard():

    buttons = [
        [types.InlineKeyboardButton(text="1", callback_data="1")],
        [types.InlineKeyboardButton(text="2", callback_data="2")],
        [types.InlineKeyboardButton(text="3", callback_data="3")],
        [types.InlineKeyboardButton(text="4", callback_data="4")],
        [types.InlineKeyboardButton(text="5", callback_data="5")],
        [types.InlineKeyboardButton(text="6", callback_data="6")],
        [types.InlineKeyboardButton(text="7", callback_data="7")],
        [types.InlineKeyboardButton(text="8", callback_data="8")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)

# Хендлер для команди /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Якщо хочеш побачити список доступних команд, введи /help")
    id_user = message.from_user.id


# Хендлер для команди /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(help_text)


# Хендлер для команди /about
@dp.message(Command("about"))
async def cmd_about(message: types.Message):
    await message.answer(about_text)


# Хендлер для команди /price
@dp.message(Command("price"))
async def cmd_price(message: types.Message):
    await message.answer(price_text)


# Хендлер для команди /pay
@dp.message(Command("pay"))
async def cmd_pay(message: types.Message):
    await message.answer(pay_text)


# Хендлер для команди /support
@dp.message(Command("support"))
async def cmd_support(message: types.Message):
    await message.answer(f"Натисніть для переходу до підтримки: {support_url}")


# Хендлер для команди /order
@dp.message(Command("order"))
async def cmd_order(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Так", callback_data="yes"))
    builder.add(types.InlineKeyboardButton(text="Ні", callback_data="no"))
    await message.answer(
        "Натисни на кнопку, щоб підтвердити дію та перейти до оформлення замовлення:",
        reply_markup=builder.as_markup()
    )


# Хендлер для callback query "no"
@dp.callback_query(lambda c: c.data == "no")
async def callback_no(query: CallbackQuery):
    await query.answer("Оформлення замовлення скасовано!")
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await bot.send_message(query.from_user.id, "Введіть команду /help, щоб ознайомитися зі списком команд.")


# Хендлер для callback query "yes"
@dp.callback_query(lambda c: c.data == "yes")
async def callback_yes(query: CallbackQuery):
    await query.answer("Оформлення замовлення розпочато!")
    id = id_user
    await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    await bot.send_message(query.from_user.id, "Оберіть предмет:", reply_markup=subject_keyboard())
    


# Хендлер для обробки вибраного предмета
@dp.callback_query(lambda c: c.data in [
    "biology", "world_history", "geography", "eng_language", "computer_science", "ua_history", "foreign_literature", "defense_ua", "maths", "ua_literature", 
    "ua_language", "chemistry", "physics", "physical_culture"
])
async def callback_subject(query: CallbackQuery):
    subject = query.data
    
    await query.answer(f"Ви вибрали: {subject}")
    await bot.send_message(query.from_user.id, f"Ваш вибір записано: {subject}")

    await bot.send_message(query.from_user.id, type_work_text, reply_markup=type_work_keyboard())

@dp.callback_query(lambda c: c.data in ["1", "2", "3", "4", "5", "6", "7", "8"])
async def callback_subject(query: CallbackQuery):
    global type_work, id, subject

    # Зберігаємо вибір користувача
    type_work = query.data
    id = query.from_user.id  # Приклад: id користувача з запиту
    subject = "Тема роботи"  # Тут можна додати ваші умови для subject

    await query.answer(f"Ви вибрали: {type_work}")
    await bot.send_message(query.from_user.id, f"Ваш вибір записано: {type_work}")
    
    # Запитуємо деталі замовлення
    await bot.send_message(query.from_user.id, 
                           "Введіть деталі замовлення, щоб Gred краще зрозумів, що вам потрібно зробити (Будь ласка, напишіть це все в одному повному повідомленні):")
    
    # Оновлюємо стан, що чекаємо на ввід користувача
    global waiting_for_input
    waiting_for_input = 'order_details'  # Тепер чекаємо на деталі замовлення

@dp.message()
async def message_input(message: types.Message):
    global waiting_for_input, order_details, comment, type_work, id, subject

    if waiting_for_input == 'order_details':  # Перевіряємо, чи ми чекаємо на деталі замовлення
        order_details = message.text
        waiting_for_input = 'comment'  # Тепер чекаємо на коментар
        await message.reply("Деталі замовлення отримано. Тепер введіть ваш коментар.")
    elif waiting_for_input == 'comment':  # Перевіряємо, чи ми чекаємо на коментар
        comment = message.text
        waiting_for_input = False  # Завершуємо процес вводу

        # Формуємо текст для відповіді
        response_text = f"ID: {id}\nSubject: {subject}\nType of Work: {type_work}\nOrder Details: {order_details}\nComment: {comment}"

        await message.reply(response_text)
    else:
        await message.reply("Вибач, але я не очікую вводу. Будь ласка, скористайтесь командою /help.")
    
    # Після обробки всіх введених даних, можна відновити очікування на нове повідомлення
    waiting_for_input = False



# Основна асинхронна функція
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
