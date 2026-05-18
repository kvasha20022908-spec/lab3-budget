# Планировщик расходов

Учебный проект по дисциплине, демонстрирующий кроссплатформенное GUI-приложение на tkinter с архитектурой MVC.

## Описание проекта

Приложение для учёта личных расходов с возможностью:
- добавления трат (сумма, категория, дата, заметка)
- визуализации расходов по категориям (гистограмма)
- просмотра итогов за выбранный период
- импорта и экспорта данных в JSON

## Структура проекта
lab3_budget/
├── model.py # Модель данных (BudgetModel)
├── view.py # Представление (BudgetGUI)
├── controller.py # Контроллер (обработчики событий)
├── main.py # Точка входа
├── requirements.txt # Зависимости
└── README.md

text

## Запуск

```bash
python main.py
Используемые технологии
Python 3

tkinter (стандартная библиотека)

JSON

Автор
Студент: Кваша Артём
Группа: укажите группу
Дисциплина: Межплатформенное программирование
Лабораторная работа №3: Кроссплатформенный GUI
Вариант 6: Планировщик расходов

text

---

## 3. Разбивка на компоненты

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
main.py
python
import tkinter as tk
from view import BudgetGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()
