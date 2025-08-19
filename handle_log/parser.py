import argparse
from typing import Namespace


def parse_arg() -> argparse.Namespace:
    """Парсер аргументов командной строки."""

    parser = argparse.ArgumentParser(description="Скрипт для обработки лог-файлов")

    parser.add_argument(
        "--file",
        type=str,
        nargs="+",
        required=True,
        help="Путь одного или нескольких лог-файлов",
    )

    parser.add_argument(
        "--report",
        type=str,
        default="average",
        choices=["average", "user_agent"],
        help="Название отчета",
    )

    parser.add_argument(
        "--date",
        type=str,
        required=False,
        help="Фильтр по дате (YYYY-MM-DD)",
    )

    return parser.parse_args()
