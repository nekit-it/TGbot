# services/storage.py
from typing import Dict, List, Optional
from uuid import uuid4

MAP_STORAGE: Dict[int, List[dict]] = {}


def save_map(
    user_id: int,
    title: str,
    depth: str,
    structure: list,
    markmap: str,
    url: Optional[str] = None,
) -> str:
    map_id = str(uuid4())

    MAP_STORAGE.setdefault(user_id, []).append(
        {
            "id": map_id,
            "title": title,
            "depth": depth,
            "structure": structure,
            "markmap": markmap,
            "url": url,
        }
    )

    return map_id


def get_user_maps(user_id: int) -> List[dict]:
    return MAP_STORAGE.get(user_id, [])


def get_last_map(user_id: int) -> Optional[dict]:
    maps = MAP_STORAGE.get(user_id) or []
    return maps[-1] if maps else None
