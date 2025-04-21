import os

import django
import telebot
from dotenv import load_dotenv
from telebot import types

from config import settings

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from django.contrib.auth import get_user_model  # NOQA E402

from borrowing.models import Borrowing  # NOQA E402

token = settings.TELEGRAM_TOKEN
if token is None:
    token = "123456:dummy"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start_handler(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_contact = types.KeyboardButton(text="Надіслати контакт", request_contact=True)
    button_ticket = types.KeyboardButton(text="Мої книги")
    keyboard.add(button_contact, button_ticket)
    bot.send_message(
        message.chat.id,
        "Привіт! Я бібліотечний бот для сповіщень і нагадувань 📚\n\n"  # NOQA E402
        "1️⃣ Натисни “Надіслати контакт”, щоб прив'язати свій акаунт\n"  # NOQA E402
        "2️⃣ Или 'Мої книги', якщо ти вже відправляв контакт раніше\n щоб дізнатися, що ти взяв і коли потрібно повернути",  # NOQA E402
        reply_markup=keyboard,
    )


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    if message.contact:
        phone_number = message.contact.phone_number
        try:
            user = get_user_model().objects.get(phone=phone_number)
            bot.send_message(message.chat.id, f"Дякую, {user.email}! Ваш контакт прийнято.")
            user.telegram_chat_id = message.chat.id
            user.save()
        except get_user_model().DoesNotExist:
            bot.send_message(message.chat.id, "Користувача з таким номером не знайдено.")
    else:
        bot.send_message(message.chat.id, "Контакт не отримано, спробуйте знову.")


@bot.message_handler(func=lambda message: message.text == "Мої книги")
def get_ticket_handler(message):
    try:
        user = get_user_model().objects.get(telegram_chat_id=message.chat.id)
    except get_user_model().DoesNotExist:
        bot.send_message(
            message.chat.id,
            "Користувача не знайдено. Будь ласка, спочатку надішліть свій контакт.",
        )
        return
    borrowing_books = Borrowing.objects.filter(user=user)
    if not borrowing_books.exists():
        bot.send_message(message.chat.id, "У вас немає заборгованих книг.")
        return

    message_text = "📚 Ваші книги:\n\n"
    for borrowing in borrowing_books:
        message_text += (
            f"{borrowing.book.title} — {borrowing.book.author}\n"
            f"Дата повернення: {borrowing.expected_return_date.strftime('%d.%m.%Y')}\n\n"
        )

    bot.send_message(message.chat.id, message_text)


if __name__ == "__main__":
    bot.polling(none_stop=True)
