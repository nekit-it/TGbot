from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import CreateMap
from services.llm import generate_markmap
from services.storage import save_map
from services.document_text import extract_text_stub
from keyboards import main_menu_keyboard

router = Router()


@router.message(CreateMap.waiting_for_llm)
async def process_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    title = data.get("title", "Без названия")
    depth = data.get("depth", "Средняя")
    source_message = data.get("source_message")

    # 1. Стартовое статус-сообщение
    status_message = await message.answer("🧠 Анализирую документ...")

    # 2. Извлекаем текст (пока заглушка)
    text = await extract_text_stub(source_message)
    try:
        await status_message.edit_text("🗺 Формирую карту...")
    except:
        pass

    # 3. Генерация карты через ИИ
    nodes = generate_markmap(text=text, depth=depth)

    # 4. Сохраняем карту
    map_id = save_map(
        user_id=message.from_user.id,
        title=title,
        depth=depth,
        structure=nodes
    )

    # 5. Финальное сообщение
    try:
        await status_message.edit_text("✅ Карта готова")
    except:
        pass

    await message.answer(
        "🗺 Результат:\n\n"
        f"Название: {title}\n"
        f"Глубина: {depth}\n\n"
        + "\n".join(f"• {n}" for n in nodes)
    )

    # 6. Сбрасываем состояние и возвращаем в меню
    await state.clear()
    await message.answer(
        "Что дальше?",
        reply_markup=main_menu_keyboard()
    )
