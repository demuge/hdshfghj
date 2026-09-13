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


# =========================
# ГЛАВНОЕ МЕНЮ
# =========================

def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("🎁 NFT-подарки", callback_data="nft"),
        ],
        [
            InlineKeyboardButton("💰 Мои покупки", callback_data="purchases"),
            InlineKeyboardButton("👤 Профиль", callback_data="profile"),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# =========================
# /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⭐ Добро пожаловать!\n\n"
        "Здесь ты сможешь покупать и продавать NFT-подарки.",
        reply_markup=main_menu(),
    )


# =========================
# КНОПКИ
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    # NFT
    if query.data == "nft":
        keyboard = [
            [
                InlineKeyboardButton(
                    "🛍 Каталог",
                    callback_data="catalog"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back"
                )
            ],
        ]

        await query.edit_message_text(
            "🎁 NFT-подарки\n\n"
            "Выбери нужный раздел:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Каталог
    elif query.data == "catalog":
        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="nft"
                )
            ]
        ]

        await query.edit_message_text(
            "🛍 Каталог\n\n"
            "Пока здесь нет товаров.\n\n"
            "Следующим этапом добавим NFT-подарки, "
            "цены и покупку.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Покупки
    elif query.data == "purchases":
        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            "💰 Мои покупки\n\n"
            "У тебя пока нет покупок.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Профиль
    elif query.data == "profile":
        user = query.from_user

        keyboard = [
            [
                InlineKeyboardButton(
                    "⬅️ Назад",
                    callback_data="back"
                )
            ]
        ]

        await query.edit_message_text(
            "👤 Профиль\n\n"
            f"ID: {user.id}\n"
            f"Username: @{user.username or 'не указан'}",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    # Назад
    elif query.data == "back":
        await query.edit_message_text(
            "⭐ Главное меню",
            reply_markup=main_menu(),
        )


# =========================
# ЗАПУСК
# =========================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("⭐ Бот запущен!")

    app.run_polling()


if __name__ == "__main__":
    main()
