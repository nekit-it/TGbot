from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo
)
from config import NETLIFY_URL

# --- Главное меню ---

def main_menu_keyboard(last_map_url: str = None):
    """
    Генерирует меню. Если есть last_map_url, кнопка ведет на карту.
    Если нет — на главную страницу (index.html).
    """
    # Если URL не передан, ведем на корень (заглушку)
    #target_url = last_map_url if last_map_url else f"https://{YC_WEBSITE_HOST}/index.html"
    target_url = last_map_url if last_map_url else NETLIFY_URL
    
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📄 Создать карту")],
            [KeyboardButton(text="📚 История")],
            [
                KeyboardButton(
                    text="🌐 Открыть мини-приложение",
                    web_app=WebAppInfo(url=target_url)
                )
            ]
        ],
        resize_keyboard=True,
    )

# --- Клавиатуры процесса ---

def depth_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Лёгкая")],
            [KeyboardButton(text="Средняя")],
            [KeyboardButton(text="Глубокая")],
        ],
        resize_keyboard=True,
    )

def llm_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Авто")],
        ],
        resize_keyboard=True,
    )

def history_keyboard(maps: list):
    keyboard = []
    for m in maps:
        # Кнопка открытия сразу в Mini App
        url = m.get('url')
        buttons = []
        
        # Если есть URL, добавляем кнопку WebApp
        if url:
             buttons.append(
                InlineKeyboardButton(
                    text=f"🌐 {m['title']}",
                    web_app=WebAppInfo(url=url)
                )
             )
        
        # Кнопка для получения текста в чат
        buttons.append(
            InlineKeyboardButton(
                text="👁 Текст",
                callback_data=f"open_map:{m['id']}",
            )
        )
        keyboard.append(buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)