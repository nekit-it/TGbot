import io
import json
import requests
import base64

from aiogram.types import Message
from config import YANDEX_API_KEY, YANDEX_FOLDER_ID, YANDEX_OCR_URL


YANDEX_OCR_URL = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"


async def _download_file_bytes(message: Message) -> bytes:
    """
    Скачиваем файл/фото из Telegram и возвращаем raw bytes.
    """
    file_obj = None

    if message.document:
        file_obj = await message.bot.get_file(message.document.file_id)
    elif message.photo:
        # берем самое большое фото
        file_obj = await message.bot.get_file(message.photo[-1].file_id)

    if not file_obj:
        return b""

    file_bytes = await message.bot.download_file(
        file_obj.file_path,
        destination=io.BytesIO()
    )
    file_bytes.seek(0)
    return file_bytes.read()


def _call_ocr(image_bytes: bytes, mime_type: str = "JPEG") -> str:
    """
    Вызов Yandex OCR и получение текста (fullText + строки).
    """
    if not image_bytes:
        return ""

    content_b64 = base64.b64encode(image_bytes).decode("utf-8")

    data = {
        "mimeType": mime_type,          # JPEG / PNG / PDF [web:3][web:8]
        "languageCodes": ["ru", "en"],  # можно ["*"] для автоопределения [web:3][web:8]
        "model": "page",
        "content": content_b64
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YANDEX_API_KEY}",  # либо Api-Key <KEY> [web:3][web:6][web:15]
        "x-folder-id": "b1gdg8n13ocirh1i6uvg",
        "x-data-logging-enabled": "true",
    }

    resp = requests.post(
        url=YANDEX_OCR_URL,
        headers=headers,
        data=json.dumps(data)
    )
    print("OCR RESPONSE:", resp.status_code, resp.text)
    resp.raise_for_status()
    result = resp.json()

    # 1) Пытаемся взять готовый fullText, если есть
    text_annotation = result.get("result", {}).get("textAnnotation", {})
    full_text = text_annotation.get("fullText")
    if full_text:
        return full_text.strip()

    # 2) Если fullText нет, собираем строки из blocks/lines
    lines = []
    for block in text_annotation.get("blocks", []):
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
        # Telegram обычно отдаёт JPEG для фото
        text = _call_ocr(image_bytes, mime_type="JPEG")
        return text or "Фотография с текстом, но OCR не вернул результат."

    if message.document:
        # Здесь можно будет добавить OCR/PDF‑парсинг позднее.
        return f"Документ: {message.document.file_name}"

    return "Неизвестный документ"