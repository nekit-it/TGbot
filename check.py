import base64
import json
import requests

# ==== НАСТРОЙКИ ====
IAM_TOKEN = "..."          # вставьте сюда ваш IAM‑токен
FOLDER_ID = "..."        # вставьте сюда идентификатор каталога
IMAGE_PATH = "..."             # путь к картинке, из которой нужно извлечь текст

# ==== ФУНКЦИЯ КОДИРОВАНИЯ ФАЙЛА В BASE64 ====
def encode_file(file_path: str) -> str:
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# ==== ПОДГОТОВКА ДАННЫХ ====
content = encode_file(IMAGE_PATH)

data = {
    "mimeType": "JPEG",             # или PNG / PDF при необходимости
    "languageCodes": ["ru", "en"],  # можно ["*"] для автоопределения
    "model": "page",                # либо "handwritten" для рукописного
    "content": content
}

url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {IAM_TOKEN}",
    "x-folder-id": FOLDER_ID,
    "x-data-logging-enabled": "true"
}

# ==== ЗАПРОС К OCR API ====
response = requests.post(url=url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.text)
response.raise_for_status()

result = response.json()

# ==== ВАРИАНТ 1: Взять готовое поле fullText ====
full_text = result["result"]["textAnnotation"]["fullText"]
print("Распознанный текст (fullText):")
print(full_text)

# ==== ВАРИАНТ 2: Пройтись по блокам/строкам и словам ====
print("\nРаспознанные строки:")
for block in result["result"]["textAnnotation"]["blocks"]:
    for line in block.get("lines", []):
        print(line["text"])


