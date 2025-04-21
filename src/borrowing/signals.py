import telebot
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from borrowing.models import Borrowing

token = settings.TELEGRAM_TOKEN
if token is None:
    token = "123456:dummy"

bot = telebot.TeleBot(token)


@receiver(post_save, sender=Borrowing)
def send_borrowing_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        if user.telegram_chat_id:
            bot.send_message(
                user.telegram_chat_id,
                f"Вы взяли книгу: {instance.book.title}\n"
                f"Вернуть до: {instance.expected_return_date.strftime('%d.%m.%Y')}",
            )


@receiver(post_save, sender=Borrowing)
def notify_book_returned(sender, instance, created, **kwargs):
    if not created and instance.actual_return_date:
        user = instance.user
        if user.telegram_chat_id:
            bot.send_message(
                user.telegram_chat_id,
                f"✅ Вы успешно вернули книгу: {instance.book.title}\n"
                f"📆 Дата возврата: {instance.actual_return_date.strftime('%d.%m.%Y')}",
            )
