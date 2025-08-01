# The log file handler
A console script for processing log files in JSON format. The script analyzes the data, aggregates it and generates reports in the form of tables.

![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Tests Passing](https://img.shields.io/badge/Tests-passing-brightgreen)
![Test Coverage](https://img.shields.io/badge/Coverage-86%25-brightgreen)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
## Функциональные требования:
- **Чтение нескольких файлов:** Поддержка нескольких аргументов ```--file```.
- **Выбор отчетов:** Добавлена опция ```--report average``` и ```--report user_agent```.
- **Фильтрация по дате:** Добавлена опция ```--date YYYY-MM-DD``` для анализа логов за конкретный день.
## Установка и запуск
1. Клонирование репозитория
```bash
git clone <your-repository-url>
```
2. Создаем и активируем виртуальное окружение:
```bash
python -m venv venv
#Windows
.\venv\Scripts\activate
#macOS/Linux
source venv/bin/activate
```
3. Установка зависимостей
```bash
pip install -r requirements.txt
```

## Примеры использования
_**1. Вызов справки**_
```bash
python main.py --help
```   
_**2. Отчет среднего времени ответа**_
```bash
python main.py --file example1.log --report average
```
<img width="588" height="203" alt="image" src="https://github.com/user-attachments/assets/9d6e58c3-3923-4fdc-b36f-dc859626590f" />

_**3. Отчет по User-Agent**_
```bash
python main.py --file example1.log --report user_agent
```
<img width="273" height="177" alt="image" src="https://github.com/user-attachments/assets/5c638e85-5506-49b6-9af8-646eef271f19" />

_**4. Отчет с фильтрацией по дате**_
```bash
python main.py --file example1.log --report average --date 2025-06-22
```
<img width="731" height="201" alt="image" src="https://github.com/user-attachments/assets/f53d040b-5905-45e2-99c5-e78463459864" />

## Тестирование
Для запуска всего набора тестов и просомтра отчета о покрытии: 
```bash
pytest --cov=main
```
<img width="399" height="136" alt="image" src="https://github.com/user-attachments/assets/21ed1868-a7e8-44bd-986c-7aa3fda3269e" />




