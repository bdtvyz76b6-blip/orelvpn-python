from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def main_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🆓 Wi-Fi"),
                KeyboardButton(text="👑 Обход Б/С")
            ],
            [
                KeyboardButton(text="👤 Личный кабинет")
            ],
            [
                KeyboardButton(text="💬 Поддержка")
            ]
        ],
        resize_keyboard=True
    )


def admin_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Выдать Обход Б/С")
            ],
            [
                KeyboardButton(text="➖ Забрать Обход Б/С")
            ],
            [
                KeyboardButton(text="👥 Пользователи")
            ],
            [
                KeyboardButton(text="⬅️ Назад")
            ]
        ],
        resize_keyboard=True
    )


def buy_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Купить",
                    callback_data="buy_bs"
                )
            ]
        ]
    )


def approve_keyboard(user_id):

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выдать",
                    callback_data=f"give_{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отказать",
                    callback_data=f"deny_{user_id}"
                )
            ]
        ]
    )