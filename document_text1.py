import io
import json
import requests

from aiogram.types import Message
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID, YANDEX_OCR_URL


async def _download_file_bytes(message: Message) -> bytes:
    """
    Скачиваем файл/фото из Telegram и возвращаем raw bytes.
    """
    file_obj = None

    if message.document:
        file_obj = await message.bot.get_file(message.document.file_id)
    elif message.photo:
        file_obj = await message.bot.get_file(message.photo[-1].file_id)

    if not file_obj:
        return b""

    file_bytes = await message.bot.download_file(file_obj.file_path, destination=io.BytesIO())
    file_bytes.seek(0)
    return file_bytes.read()


def _call_ocr(image_bytes: bytes, mime_type: str = "image/jpeg") -> str:
    """
    Вызов Yandex Vision OCR и склейка текста.
    """
    if not image_bytes:
        return ""

    import base64

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json",
        "x-folder-id": YANDEX_FOLDER_ID,
    }

    # Формат тела по TextRecognition.Recognize [web:37][web:36]
    body = {
        "mimeType": mime_type,
        "languageCodes": ["ru", "en"],
        "model": "page",  # полнотекстовый OCR
        "content": image_b64,
    }

    resp = requests.post(YANDEX_OCR_URL, headers=headers, data=json.dumps(body))
    print("OCR RESPONSE:", resp.status_code, resp.text)
    resp.raise_for_status()
    data = resp.json()

    lines = []
    for page in data.get("result", {}).get("pages", []):
        for block in page.get("blocks", []):
            for line in block.get("lines", []):
                txt = line.get("text", "").strip()
                if txt:
                    lines.append(txt)

    return "\n".join(lines)


async def extract_text(message: Message) -> str:
    """
    Универсальная функция:
    - если фото → OCR
    - если документ (pdf/docx) → пока заглушка по имени файла
    """
    if message.photo:
        image_bytes = await _download_file_bytes(message)
        text = _call_ocr(image_bytes, mime_type="image/jpeg")
        return text or "Фотография с текстом, но OCR не вернул результат."

    if message.document:
        # В MVP просто кратко описываем документ;
        # сюда позже можно добавить парсинг PDF/DOCX.
        return f"Документ: {message.document.file_name}"

    return "Неизвестный документ"
