import json
from datetime import datetime
from typing import List, Dict, Any, Optional


def read_logs(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Читает и парсит JSON-строки из файлов."""
    logs: List[Dict[str, Any]] = []
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        print(f"Ошибка: Невалидный JSON в файле {file_path}")
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден {file_path}")

    return logs


def filter_data_logs(
    logs: List[Dict[str, Any]], date_str: Optional[str]
) -> List[Dict[str, Any]]:
    """Фильтрует логи по дате (YYYY-MM-DD)."""
    if not date_str:
        return logs
    try:
        filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Ошибка: Измените формат даты на YYYY-MM-DD")
        return logs

    result: List[Dict[str, Any]] = []
    for log in logs:
        ts = log.get("@timestamp")
        if not ts:
            continue
        try:
            entry_date = datetime.fromisoformat(ts).date()
            if entry_date == filter_date:
                result.append(log)
        except (ValueError, TypeError):
            continue

    return result
