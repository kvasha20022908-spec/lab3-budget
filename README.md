# Планировщик расходов

Учебный проект по дисциплине, демонстрирующий кроссплатформенное GUI-приложение на tkinter с архитектурой MVC.

## Описание проекта

Приложение для учёта личных расходов с возможностью:

- добавления трат (сумма, категория, дата, заметка)
- визуализации расходов по категориям (гистограмма)
- просмотра итогов за выбранный период
- импорта и экспорта данных в JSON

Приложение использует архитектуру MVC (Model-View-Controller):

- Model — класс BudgetModel: хранение и обработка данных
- View — класс BudgetGUI: графический интерфейс на tkinter
- Controller — методы-обработчики внутри View

## Структура проекта

```
lab3_budget/
├── main.py
├── model.py
├── view.py
├── requirements.txt
├── expenses.json
└── README.md
```

## Запуск

```
python main.py
```

## Функционал

### Вкладка "Расходы"

- Таблица всех трат (сумма, категория, дата, заметка)
- Форма добавления нового расхода
- Кнопка удаления выбранного расхода
- Автоматический подсчёт общей суммы

### Вкладка "По категориям"

- Гистограмма распределения расходов по категориям
- Текстовый отчёт с суммами и процентами

### Вкладка "Итоги за период"

- Фильтрация по датам (с — по)
- Таблица расходов за выбранный период
- Итоговая сумма за период

### Меню

- Импорт из JSON
- Экспорт в JSON
- Автосохранение при выходе

## Категории расходов

| Категория | Цвет |
|-----------|------|
| Продукты | #7c5cbf |
| Транспорт | #5c8abf |
| Жильё | #bf5c7c |
| Развлечения | #5cbf8a |
| Здоровье | #bf8a5c |
| Одежда | #8a5cbf |
| Связь | #5cbfbf |
| Образование | #b5bf5c |
| Другое | #a0a0a0 |

## Используемые технологии

- Python 3
- tkinter (стандартная библиотека)
- JSON

## Обеспечение кроссплатформенности

- tkinter входит в стандартную библиотеку Python на всех платформах
- Кодировка UTF-8 при сохранении JSON
- Не используется системно-зависимых вызовов

  

## Автор

Студент: Кваша В.И

Группа: ИСИТ-31

Дисциплина: Межплатформенное программирование

Лабораторная работа №3: Кроссплатформенный GUI

Вариант 6: Планировщик расходов

---

## Разбивка на компоненты

### `model.py`
```python
import json
import os

class BudgetModel:
    CATEGORIES = ["Продукты", "Транспорт", "Жильё", "Развлечения", "Здоровье", "Одежда", "Связь", "Образование", "Другое"]

    def __init__(self):
        self.expenses = []
        self.filename = "expenses.json"

    def add_expense(self, amount, category, date, note):
        self.expenses.append({"amount": float(amount), "category": category, "date": date, "note": note.strip()})

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]

    def get_total(self, expenses=None):
        data = expenses if expenses is not None else self.expenses
        return sum(e["amount"] for e in data)

    def get_by_category(self):
        result = {}
        for e in self.expenses:
            result[e["category"]] = result.get(e["category"], 0) + e["amount"]
        return sorted(result.items(), key=lambda x: x[1], reverse=True)

    def get_by_period(self, date_from, date_to):
        return [e for e in self.expenses if date_from <= e["date"] <= date_to]

    def save_to_file(self, filename=None):
        path = filename or self.filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename=None):
        path = filename or self.filename
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.expenses = json.load(f)
