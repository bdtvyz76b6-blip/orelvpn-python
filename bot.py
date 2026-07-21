import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import (
    BOT_TOKEN,
    WIFI_LINK,
    BS_LINK,
    FREE_TARIFF,
    PAID_TARIFF,
    SUPPORT,
    ADMIN_ID,
    CARD_NUMBER,
    CARD_OWNER,
    PRICE_BS
)

from database import (
    create_table,
    add_user,
    set_tariff,
    get_user,
    get_all_users,
    remove_bs
)

from keyboards import (
    main_menu,
    admin_menu,
    buy_keyboard,
    approve_keyboard
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class AdminStates(StatesGroup):
    add_bs = State()
    remove_bs = State()


# START
@dp.message(Command("start"))
async def start(message: types.Message):

    add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🦅 Орёл VPN\n\n"
        "Выберите раздел:",
        reply_markup=main_menu()
    )


# WI-FI
@dp.message(lambda m: m.text == "🆓 Wi-Fi")
async def wifi(message: types.Message):

    set_tariff(
        message.from_user.id,
        FREE_TARIFF,
        WIFI_LINK
    )

    await message.answer(
        "🆓 Wi-Fi\n\n"
        "Ваша ссылка:\n\n"
        f"{WIFI_LINK}"
    )


# ОБХОД Б/С
@dp.message(lambda m: m.text == "👑 Обход Б/С")
async def bypass(message: types.Message):

    user = get_user(message.from_user.id)

    if user and user[2] == PAID_TARIFF:

        await message.answer(
            "👑 Обход Б/С активен\n\n"
            f"{BS_LINK}"
        )

    else:

        await message.answer(
            "👑 Обход Б/С\n\n"
            f"Стоимость: {PRICE_BS}\n\n"
            "Для покупки нажмите кнопку:",
            reply_markup=buy_keyboard()
        )


# ЛИЧНЫЙ КАБИНЕТ
@dp.message(lambda m: m.text == "👤 Личный кабинет")
async def cabinet(message: types.Message):

    user = get_user(message.from_user.id)

    if user:

        bs_status = "Активен" if user[2] == PAID_TARIFF else "Не активен"
        bs_link = BS_LINK if user[2] == PAID_TARIFF else "Нет доступа"

        await message.answer(
            "👤 Личный кабинет\n\n"
            f"🆔 ID: {user[0]}\n\n"
            "🆓 Wi-Fi: Активен\n"
            f"🔗 {WIFI_LINK}\n\n"
            f"👑 Обход Б/С: {bs_status}\n"
            f"🔗 {bs_link}"
        )


# ПОДДЕРЖКА
@dp.message(lambda m: m.text == "💬 Поддержка")
async def support(message: types.Message):

    await message.answer(
        "💬 Поддержка:\n\n"
        f"{SUPPORT}"
    )


# ПОКУПКА
@dp.callback_query(lambda c: c.data == "buy_bs")
async def buy_bs(callback: types.CallbackQuery):

    await callback.message.answer(
        "👑 Покупка Обход Б/С\n\n"
        f"Цена: {PRICE_BS}\n\n"
        "💳 Реквизиты:\n"
        f"{CARD_NUMBER}\n\n"
        f"Получатель: {CARD_OWNER}\n\n"
        "После оплаты отправьте сюда скриншот."
    )

    try:
        await bot.send_message(
            ADMIN_ID,
            "🛒 Новая заявка\n\n"
            f"🆔 ID: {callback.from_user.id}\n"
            f"👤 @{callback.from_user.username}"
        )
    except Exception as e:
        print("Ошибка отправки админу:", e)


# ПОЛУЧЕНИЕ ЧЕКА
@dp.message(lambda m: m.photo)
async def check_photo(message: types.Message):

    try:
        await bot.send_photo(
            ADMIN_ID,
            message.photo[-1].file_id,
            caption=
            "📷 Новый чек\n\n"
            f"🆔 ID: {message.from_user.id}\n"
            f"👤 @{message.from_user.username}",
            reply_markup=approve_keyboard(
                message.from_user.id
            )
        )

        await message.answer(
            "✅ Чек отправлен.\n"
            "Ожидайте проверки."
        )

    except Exception as e:
        print("Ошибка отправки чека админу:", e)
        await message.answer(
            "❌ Ошибка отправки чека."
        )


# ПОДТВЕРЖДЕНИЕ ЧЕКА
@dp.callback_query(lambda c: c.data.startswith("give_"))
async def give_access(callback: types.CallbackQuery):

    user_id = int(callback.data.split("_")[1])

    set_tariff(
        user_id,
        PAID_TARIFF,
        BS_LINK
    )

    await callback.message.edit_caption(
        caption=
        callback.message.caption + "\n\n✅ Оплата подтверждена"
    )

    try:
        await bot.send_message(
            user_id,
            "🎉 Вам активировали тариф!\n\n"
            "👑 Обход Б/С\n\n"
            "Ваша ссылка:\n"
            f"{BS_LINK}"
        )
    except:
        pass

    await callback.answer("Доступ выдан")


@dp.callback_query(lambda c: c.data.startswith("deny_"))
async def deny_access(callback: types.CallbackQuery):

    user_id = int(callback.data.split("_")[1])

    await callback.message.edit_caption(
        caption=
        callback.message.caption + "\n\n❌ Оплата отклонена"
    )

    try:
        await bot.send_message(
            user_id,
            "❌ Ваша оплата не была подтверждена."
        )
    except:
        pass

    await callback.answer("Заявка отклонена")


# =================
# АДМИНКА
# =================

@dp.message(Command("admin"))
async def admin(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🛠 Админ-панель",
        reply_markup=admin_menu()
    )


# ВЫДАТЬ
@dp.message(lambda m: m.text == "➕ Выдать Обход Б/С")
async def add_button(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Введите ID пользователя:"
    )

    await state.set_state(
        AdminStates.add_bs
    )


@dp.message(AdminStates.add_bs)
async def add_process(message: types.Message, state: FSMContext):

    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer(
            "Главное меню",
            reply_markup=main_menu()
        )
        return

    if not message.text.isdigit():
        await message.answer(
            "Введите только ID пользователя цифрами."
        )
        return

    user_id = int(message.text)

    set_tariff(
        user_id,
        PAID_TARIFF,
        BS_LINK
    )

    await message.answer(
        "✅ Выдано",
        reply_markup=admin_menu()
    )

    try:
        await bot.send_message(
            user_id,
            "🎉 Вам активировали:\n\n"
            "👑 Обход Б/С\n\n"
            f"{BS_LINK}"
        )
    except:
        pass

    await state.clear()


# ЗАБРАТЬ
@dp.message(lambda m: m.text == "➖ Забрать Обход Б/С")
async def remove_button(message: types.Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "Введите ID пользователя:"
    )

    await state.set_state(
        AdminStates.remove_bs
    )


@dp.message(AdminStates.remove_bs)
async def remove_process(message: types.Message, state: FSMContext):

    if message.text == "⬅️ Назад":
        await state.clear()
        await message.answer(
            "Главное меню",
            reply_markup=main_menu()
        )
        return

    if not message.text.isdigit():
        await message.answer(
            "Введите только ID пользователя цифрами."
        )
        return

    user_id = int(message.text)

    remove_bs(user_id)

    await message.answer(
        "✅ Доступ отключён",
        reply_markup=admin_menu()
    )

    await state.clear()


# ПОЛЬЗОВАТЕЛИ
@dp.message(lambda m: m.text == "👥 Пользователи")
async def users(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    text = "👥 Пользователи:\n\n"

    for user in get_all_users():

        text += (
            f"🆔 {user[0]}\n"
            f"📌 {user[2]}\n\n"
        )

    await message.answer(text)


# НАЗАД
@dp.message(lambda m: m.text == "⬅️ Назад")
async def back(message: types.Message, state: FSMContext):

    await state.clear()

    await message.answer(
        "Главное меню",
        reply_markup=main_menu()
    )


async def main():

    create_table()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())