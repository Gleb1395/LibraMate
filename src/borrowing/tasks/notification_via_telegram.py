from datetime import date

import telebot
from celery import shared_task
from django.utils import timezone

from borrowing.models import Borrowing
from config import settings

token = settings.TELEGRAM_TOKEN
if token is None:
    token = "123456:dummy"

bot = telebot.TeleBot(token)


@shared_task
def check_overdue_borrowings():
    today = date.today()
    overdue = Borrowing.objects.filter(
        is_active=True,
        expected_return_date__lte=today,
        actual_return_date__isnull=True,
    ).select_related("user", "book")

    for borrowing in overdue:
        send_overdue_notification.delay(borrowing.id)


@shared_task
def send_overdue_notification(borrowing_id):

    borrowing = Borrowing.objects.get(pk=borrowing_id)
    days_overdue = timezone.now().date() - borrowing.expected_return_date
    fine_for_overdue_book = days_overdue.days * borrowing.book.daily_fee
    text = (
        f"Прострочено!\n"
        f"{borrowing.user.email}\n"
        f"{borrowing.book.title}\n"
        f"Повернення мало бути: {borrowing.expected_return_date}\n"
        f"Вам буде нараховано штраф у розмірі: {fine_for_overdue_book}\n"
    )
    bot.send_message(chat_id=borrowing.user.telegram_chat_id, text=text)
