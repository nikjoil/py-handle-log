import argparse
import json
# defauldict автоматическая инициализация несуществующих ключей значением 
# по умолчанию. Это упрощает такие задачи, как подсчёт и 
# группировка в словарях.
from collections import defaultdict
from datetime import datetime
from abc import ABC, abstractmethod
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
        choices=['average', 'user_agent'], # разрешены только значения из списка
        help='Название отчета'
    )

    # Правило: --date
    parser.add_argument(
        '--date',
        type=str,
        required=False,
        help='Фильтр по дате'
    )

    return parser.parse_args()


def read_logs(file_paths):
    """Читает и парсит JSON из лог-файлов"""
    logs = []
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    if line.strip():
                        logs.append(json.loads(line))
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден {file_path}")
        except json.JSONDecodeError:
            print(f"Ошибка: Невалидный JSON {file_path}")
    
    return logs

def filter_data_logs(logs, date_str):
    """Фильтр логов по дате"""
    if not date_str:
        return logs
    
    try: 
        filter_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"Ошибка: Измените формат даты на YYYY-MM-DD")
        return logs
    
    filter_log = []

    for log in logs:
        log_date_str = log.get("@timestamp")
        if not log_date_str:
            continue

        try:
            entry_date = datetime.fromisoformat(log_date_str).date()
            if entry_date == filter_date:
                filter_log.append(log)
        except (ValueError, TypeError):
            continue
    
    return filter_log


class GenReport(ABC):
    """Базовый класс для отчетов"""

    @abstractmethod
    def process_log(self, logs):
        """Обработка сырых логов"""
        pass

    @abstractmethod
    def render_report(self, processed_data, report_date=None):
        """Обработанные логи -> таблица"""
        pass


class AverageTimeReport(GenReport):
    """"""
    
    def process_log(self, logs):
        """Считываем запрос и складываем время ответа"""
        endpoints_data = defaultdict(lambda: {'count': 0, 'total_time': 0.0})
        
        for log_entry in logs:
            # Извлекаем данные из словаря
            endpoint = log_entry.get('url')
            response_time = log_entry.get('response_time')
            # Если есть endpoint и время ответа(число)
            if endpoint and isinstance(response_time, (int, float)):
                endpoints_data[endpoint]['count'] += 1
                endpoints_data[endpoint]['total_time'] += response_time

        return endpoints_data


    def render_report(self, processed_data, report_date=None):
        """Среднее время и подготовка данных"""
        report = []
        
        for endpoint, value in processed_data.items():
            if value['count'] > 0:
                average_time = value['total_time'] / value['count']
                report.append([
                    endpoint,
                    value['count'],
                    round(average_time, 3)
                ])

        headers = ["handler", "total", "avg_response_time"]
        report_title = "Отчет c количеством запросов и средним временем ответа"

        if report_date: 
            report_title += f" за {report_date}"

        return report_title, report, headers    
    

class UserAgentRep(GenReport):
    """Используемый браузер"""

    def process_log(self, logs):
        """Счетчик встречи браузеров в логах"""
        browser_counts = defaultdict(int)

        for log in logs:
            user_agent_str = log.get("http_user_agent")
            
            if user_agent_str and user_agent_str != "...":
                if "Chrome/" in user_agent_str and "Safari/" in user_agent_str:
                    browser_counts["Chrome"] += 1
                elif "Firefox/" in user_agent_str:
                    browser_counts["Firefox"] += 1
                elif "Safari/" in user_agent_str:
                    browser_counts['Safari'] += 1
                else:
                    browser_counts["Other"] += 1
        
        return browser_counts
    

    def render_report(self, processed_data, report_date=None):
        report_data = list(processed_data.items())
        headers = ["User-Agent", "total"]
        report_title = "Отчет по браузерам"

        if report_date:
            report_title += f" за {report_date}"

        return report_title, report_data, headers


REPORT = {
    'average': AverageTimeReport,
    'user_agent': UserAgentRep,
}


def main():
    args = parse_arg()
    logs = read_logs(args.file)
    filter_logs = filter_data_logs(logs, args.date)

    if not filter_logs:
        print(f"Нет логов для даты: {args.data}")
        return
    
    report_class = REPORT.get(args.report)

    if not report_class:
        print(f"Ошибка: отчет '{args.report}' не найден")
        return
    
    report_gen = report_class()
    processed_data = report_gen.process_log(filter_logs)
    report_title, table_data, headers = report_gen.render_report(
        processed_data,
        report_date=args.date
        )
    
    print(f"\n{report_title}\n")
    print(tabulate(table_data, headers=headers))

if __name__ == "__main__":
    main()