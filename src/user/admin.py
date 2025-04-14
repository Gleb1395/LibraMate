from django.contrib import admin
from django.contrib.auth import get_user_model


@admin.register(get_user_model())
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "telegram_chat_id", "phone")
