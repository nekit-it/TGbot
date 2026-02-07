from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from uuid import uuid4

from states import CreateMap
from services.llm import generate_markmap
from services.storage import save_map
from services.document_text import extract_text
from services.github_storage import upload_to_github # <-- Новый импорт
from keyboards import main_menu_keyboard

router = Router()

@router.message(CreateMap.waiting_for_llm)
async def process_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    depth = data.get("depth", "Средняя")
    source_message = data.get("source_message")

    status_message = await message.answer("🧠 Анализирую документ...")

    text = await extract_text(source_message)
    try:
        await status_message.edit_text("🗺 Формирую структуру...")
    except Exception:
        pass

    # Генерация контента
    result = generate_markmap(text=text, depth=depth)
    
    # Генерируем уникальное имя файла
    filename = f"{uuid4()}.md"

    # Загрузка на GitHub и получение ссылки
    public_url = None
    try:
        await status_message.edit_text("☁️ Сохраняю...")
        # Загружаем только Markmap Markdown, HTML сгенерируется на клиенте (Netlify)
        public_url = upload_to_github(result["markmap"], filename)
    except Exception as e:
        print(f"Github Upload Error: {e}")
        await message.answer(f"⚠️ Ошибка сохранения в облако: {e}")

    # Сохраняем в локальную БД бота
    save_map(
        user_id=message.from_user.id,
        title=result["title"],
        depth=depth,
        structure=result["nodes"],
        markmap=result["markmap"],
        url=public_url,
    )

    try:
        await status_message.delete()
    except Exception:
        pass

    # Кнопка для конкретной карты
    inline_kb = None
    if public_url:
        inline_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Открыть карту", web_app=WebAppInfo(url=public_url))]
        ])

    await message.answer(
        f"✅ <b>Карта готова:</b> {result['title']}",
        reply_markup=inline_kb,
        parse_mode="HTML"
    )

    # Обновляем главное меню с ссылкой на последнюю карту
    await state.clear()
    await message.answer(
        "Карта сохранена.",
        reply_markup=main_menu_keyboard(last_map_url=public_url)
    )