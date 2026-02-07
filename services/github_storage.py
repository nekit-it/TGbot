import base64
import requests
from uuid import uuid4
from config import GITHUB_TOKEN, GITHUB_REPO, NETLIFY_URL

def upload_to_github(text_content: str, filename: str) -> str:
    """
    Загружает текст (Markdown) в репозиторий GitHub и возвращает ссылку на Netlify Viewer.
    """
    path = f"maps/{filename}"
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    
    # GitHub API требует base64 контент
    content_bytes = text_content.encode('utf-8')
    base64_content = base64.b64encode(content_bytes).decode('utf-8')
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "message": f"Add map {filename}",
        "content": base64_content,
        "branch": "main"  # или "master", проверьте свою ветку
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code not in [200, 201]:
        print(f"GitHub Error: {response.text}")
        raise Exception(f"Ошибка загрузки на GitHub: {response.status_code}")
        
    # Формируем ссылку для Netlify
    # Мы передаем ID файла в Viewer, который сам скачает контент с GitHub Raw
    return f"{NETLIFY_URL}/?map={filename}"