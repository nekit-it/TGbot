# services/html_export.py
from pathlib import Path

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <title>{title}</title>
  <style>
    body {{ margin: 0; font-family: system-ui, sans-serif; background: #111; color: #eee; }}
    .container {{ padding: 16px; }}
    h2 {{ margin-top: 0; }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.15.3"></script>
</head>
<body>
  <div class="container">
    <h2>🗺 {title}</h2>
    <pre class="markmap">
{markmap}
    </pre>
  </div>
</body>
</html>
"""


def save_markmap_html(title: str, markmap: str, output_dir: str = "export") -> str:
    """
    Генерирует HTML-файл с Markmap и сохраняет локально.
    Возвращает путь к файлу.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    safe_title = "".join(c for c in title if c.isalnum() or c in " _-").strip() or "map"
    filename = f"{safe_title}.html"
    path = output_path / filename

    html = HTML_TEMPLATE.format(title=title, markmap=markmap)
    path.write_text(html, encoding="utf-8")

    return str(path)
