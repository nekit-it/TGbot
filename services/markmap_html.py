from pathlib import Path

# Улучшенный шаблон с поддержкой Telegram WebApp цветов и адаптивности
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>{title}</title>
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--tg-theme-bg-color, #111);
      color: var(--tg-theme-text-color, #eee);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .header {{
      padding: 10px 16px;
      background-color: var(--tg-theme-secondary-bg-color, #222);
      border-bottom: 1px solid var(--tg-theme-hint-color, #333);
      font-weight: 600;
      font-size: 16px;
      text-align: center;
      flex-shrink: 0;
    }}
    .markmap-container {{
      flex-grow: 1;
      width: 100%;
      height: 100%;
    }}
    svg {{
      width: 100%;
      height: 100%;
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-view@0.15.3"></script>
  <script src="https://cdn.jsdelivr.net/npm/markmap-autoloader@0.15.3"></script>
</head>
<body>
  <div class="header">{title}</div>
  <div class="markmap-container">
    <div class="markmap">
{markmap}
    </div>
  </div>
  <script>
    // Сообщаем Телеграму, что приложение готово
    if (window.Telegram && window.Telegram.WebApp) {{
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();
    }}
  </script>
</body>
</html>
"""

def md_to_markmap_html(markdown: str, html_path: str, title: str = "Mindmap") -> str:
    """
    Создаёт HTML-файл с Markmap для загрузки на хостинг.
    """
    path = Path(html_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Экранируем обратные слеши, если они есть в markdown, чтобы JS не ломался
    safe_markdown = markdown.replace('\\', '\\\\').replace('`', '\`')

    html = HTML_TEMPLATE.format(title=title, markmap=safe_markdown)
    path.write_text(html, encoding="utf-8")
    return str(path)