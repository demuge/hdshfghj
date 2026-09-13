import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден")


def main_menu():
    keyboard = [
        [InlineKeyboardButton("🎁 NFT-подарки", callback_data="nft")],
        [
            InlineKeyboardButton("💰 Мои покупки", callback_data="purchases"),
            InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ Добро пожаловать!\n\n"
        "Здесь можно покупать и продавать NFT-подарки.",
        reply_markup=main_menu(),
    )


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "nft":
        keyboard = [
            [InlineKeyboardButton("🛍 Каталог", callback_data="catalog")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")],
        ]

        await query.edit_message_text(
            "🎁 NFT-подарки\n\n"
            "Выбери нужный раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "catalog":
        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="nft")]
        ]

        await query.edit_message_text(
            "🛍 Каталог\n\n"
            "Каталог пока пуст.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "purchases":
        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
        ]

        await query.edit_message_text(
            "💰 Мои покупки\n\n"
            "Покупок пока нет.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "profile":
        user = query.from_user

        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
        ]

        await query.edit_message_text(
            "👤 Профиль\n\n"
            f"ID: {user.id}\n"
            f"Username: @{user.username or 'не указан'}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        await query.edit_message_text(
            "⭐ Главное меню",
            reply_markup=main_menu(),
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("⭐ Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
