import argparse
import json
# defauldict автоматическая инициализация несуществующих ключей значением 
# по умолчанию. Это упрощает такие задачи, как подсчёт и 
# группировка в словарях.
from collections import defaultdict
from tabulate import tabulate


def parse_arg():
    """Функция для разбора арг. ком. строки"""
    # Объект парсер, description при вызове --help
    parser = argparse.ArgumentParser(description='Скрипт для обработки лог-файлов')
    
    # Добавление правил (аргументов):
    # Правило: --file
    parser.add_argument(
        '--file',
        type=str,
        nargs='+', # + значит один или более, * ноль или больше
        required=True,  # инструкция (правило) обязательное
        help='Путь одного или нескольких лог-файлов'
    )

    # Правило: --report
    parser.add_argument(
        '--report',
        type=str,
        default='average',
        choices=['average'], # разрешены только значения из списка
        help='Название отчета'
    )

    return parser.parse_args()


def read_parse_logs(file_paths):
    """Читает и парсит JSON из лог-файлов"""
    logs = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                file_logs = json.load(f) # список словарей
                logs.extend(file_logs) # extend добавляет по отдельности, а append как ОДИН элемент
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден {file_path}")
        except json.JSONDecodeError:
            print(f"Ошибка: Невалидный JSON {file_path}")
    
    return logs


def process_data(logs):
    """Считываем запрос и складываем время ответа"""
    endpoints_data = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
    
    for log_entry in logs:
        # Извлекаем данные из словаря
        endpoint = log_entry.get('endpoint')
        response_time = log_entry.get('response_time')
        # Если есть endpoint и время ответа(число)
        if endpoint and isinstance(response_time, (int, float)):
            endpoints_data[endpoint]['count'] += 1
            endpoints_data[endpoint]['total_time'] += response_time

    return endpoints_data


def prepare_report_data(process_data):
    """Среднее время и подготовка данных"""
    report = []
    
    for endpoint, value in process_data.items():
        if value['count'] > 0:
            average_time = value['total_time'] / value['count']
            report.append([
                endpoint,
                value['count'],
                round(average_time, 3)
            ])

    return report


def main():
    args = parse_arg()
    
    if args.report == 'average':
        all_logs = read_parse_logs(args.file)
        if not all_logs:
            print("Нет логов для обработки")
            return
        process_data = process_data(all_logs)
        report_data = prepare_report_data(process_data)
        
        headers = ["handler", "total", "avg_response_time"]
        print(tabulate(report_data, headers=headers, tablefmt="grid"))
    else:
        print(f"Другие отчеты!")

if __name__ == "__main__":
    main()