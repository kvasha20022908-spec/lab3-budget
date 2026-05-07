#!/usr/bin/env python3
"""
Лабораторная работа №3 — Вариант 6
Планировщик расходов: добавление трат, визуализация, итоги за период.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime


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


class BudgetGUI:
    BG_MAIN = "#f5f0ff"
    BG_CARD = "#ffffff"
    BG_HEADER = "#e8deff"
    FG_TITLE = "#4a3070"
    FG_TEXT = "#3a3050"
    FG_ACCENT = "#7c5cbf"
    FG_ACCENT2 = "#9b7fd4"

    CAT_COLORS = {
        "Продукты": "#7c5cbf", "Транспорт": "#5c8abf", "Жильё": "#bf5c7c",
        "Развлечения": "#5cbf8a", "Здоровье": "#bf8a5c", "Одежда": "#8a5cbf",
        "Связь": "#5cbfbf", "Образование": "#b5bf5c", "Другое": "#a0a0a0",
    }

    def __init__(self, root):
        self.root = root
        self.root.title("Планировщик расходов")
        self.root.geometry("960x680")
        self.root.configure(bg=self.BG_MAIN)
        self._setup_styles()
        self.model = BudgetModel()
        self.model.load_from_file()
        self.var_amount = tk.StringVar()
        self.var_category = tk.StringVar(value="Продукты")
        self.var_date = tk.StringVar(value=datetime.today().strftime("%Y-%m-%d"))
        self.var_note = tk.StringVar()
        self.var_from = tk.StringVar()
        self.var_to = tk.StringVar()
        self._build_menu()
        self._build_notebook()
        self._refresh_all()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=self.BG_MAIN, foreground=self.FG_TEXT, font=("Segoe UI", 10))
        style.configure("TFrame", background=self.BG_MAIN)
        style.configure("TLabel", background=self.BG_MAIN, foreground=self.FG_TEXT)
        style.configure("TLabelframe", background=self.BG_CARD, foreground=self.FG_TITLE, borderwidth=1, relief="solid")
        style.configure("TLabelframe.Label", background=self.BG_CARD, foreground=self.FG_TITLE, font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background=self.BG_MAIN, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.BG_HEADER, foreground=self.FG_TEXT, padding=(16, 8), font=("Segoe UI", 10))
        style.map("TNotebook.Tab", background=[("selected", self.BG_CARD)], foreground=[("selected", self.FG_TITLE)])
        style.configure("TButton", background=self.BG_HEADER, foreground=self.FG_TEXT, borderwidth=0, padding=(14, 6))
        style.configure("Add.TButton", background=self.FG_ACCENT, foreground="#ffffff", borderwidth=0, padding=(14, 6), font=("Segoe UI", 9, "bold"))
        style.map("Add.TButton", background=[("active", "#6a4db5")])
        style.configure("Del.TButton", background="#c0b0d0", foreground=self.FG_TITLE, borderwidth=0, padding=(12, 6))
        style.configure("TEntry", fieldbackground=self.BG_CARD, foreground=self.FG_TEXT, borderwidth=1, padding=7)
        style.configure("TCombobox", fieldbackground=self.BG_CARD, foreground=self.FG_TEXT)
        self.root.option_add("*TCombobox*Listbox*Background", self.BG_CARD)
        self.root.option_add("*TCombobox*Listbox*Foreground", self.FG_TEXT)
        style.configure("Treeview", background=self.BG_MAIN, foreground=self.FG_TEXT, fieldbackground=self.BG_MAIN, rowheight=28, borderwidth=0)
        style.configure("Treeview.Heading", background=self.BG_HEADER, foreground=self.FG_TITLE, padding=(10, 6), borderwidth=0, font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", self.FG_ACCENT2)], foreground=[("selected", "#ffffff")])

    def _build_menu(self):
        menubar = tk.Menu(self.root, bg=self.BG_HEADER, fg=self.FG_TEXT, activebackground=self.FG_ACCENT2, borderwidth=0)
        file_menu = tk.Menu(menubar, tearoff=0, bg=self.BG_HEADER, fg=self.FG_TEXT)
        file_menu.add_command(label="Импорт из JSON...", command=self._import)
        file_menu.add_command(label="Экспорт в JSON...", command=self._export)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._on_close)
        menubar.add_cascade(label="Файл", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0, bg=self.BG_HEADER, fg=self.FG_TEXT)
        help_menu.add_command(label="О программе", command=self._about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        self.root.config(menu=menubar)

    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self.tab_expenses = ttk.Frame(self.notebook)
        self.tab_summary = ttk.Frame(self.notebook)
        self.tab_period = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_expenses, text="  Расходы  ")
        self.notebook.add(self.tab_summary, text="  По категориям  ")
        self.notebook.add(self.tab_period, text="  Итоги за период  ")
        self._build_expenses_tab()
        self._build_summary_tab()
        self._build_period_tab()

    def _build_expenses_tab(self):
        frame = ttk.Frame(self.tab_expenses, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)
        form = ttk.LabelFrame(frame, text=" Добавить расход ", padding=14)
        form.pack(fill=tk.X, pady=(0, 12))
        ttk.Label(form, text="Сумма:").grid(row=0, column=0, sticky=tk.W, padx=6, pady=4)
        ttk.Entry(form, textvariable=self.var_amount, width=14).grid(row=0, column=1, padx=6)
        ttk.Label(form, text="Категория:").grid(row=0, column=2, sticky=tk.W, padx=6, pady=4)
        ttk.Combobox(form, textvariable=self.var_category, values=BudgetModel.CATEGORIES, state="readonly", width=16).grid(row=0, column=3, padx=6)
        ttk.Label(form, text="Дата:").grid(row=0, column=4, sticky=tk.W, padx=6, pady=4)
        ttk.Entry(form, textvariable=self.var_date, width=14).grid(row=0, column=5, padx=6)
        ttk.Label(form, text="Заметка:").grid(row=1, column=0, sticky=tk.W, padx=6, pady=4)
        ttk.Entry(form, textvariable=self.var_note, width=30).grid(row=1, column=1, columnspan=3, padx=6)
        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=1, column=4, columnspan=2, sticky=tk.E, padx=6, pady=6)
        ttk.Button(btn_frame, text="Добавить", command=self._add_expense, style="Add.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Удалить", command=self._delete_expense, style="Del.TButton").pack(side=tk.LEFT, padx=5)
        self.lbl_total = ttk.Label(frame, text="Итого: 0 руб.", font=("Segoe UI", 12, "bold"), foreground=self.FG_TITLE)
        self.lbl_total.pack(anchor=tk.W, pady=(0, 8))
        cols = ("amount", "category", "date", "note")
        self.tree_exp = ttk.Treeview(frame, columns=cols, show="headings", selectmode="browse")
        self.tree_exp.heading("amount", text="Сумма")
        self.tree_exp.heading("category", text="Категория")
        self.tree_exp.heading("date", text="Дата")
        self.tree_exp.heading("note", text="Заметка")
        self.tree_exp.column("amount", width=100)
        self.tree_exp.column("category", width=130)
        self.tree_exp.column("date", width=110)
        self.tree_exp.column("note", width=300)
        self.tree_exp.pack(fill=tk.BOTH, expand=True)

    def _build_summary_tab(self):
        frame = ttk.Frame(self.tab_summary, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="Распределение расходов по категориям", font=("Segoe UI", 14, "bold"), foreground=self.FG_TITLE).pack(pady=(0, 14))
        self.canvas = tk.Canvas(frame, bg=self.BG_CARD, height=300, highlightthickness=1, highlightbackground="#ddd")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self.text_summary = tk.Text(frame, height=8, bg=self.BG_CARD, fg=self.FG_TEXT, font=("Consolas", 10), borderwidth=1, relief="solid", padx=10, pady=10)
        self.text_summary.pack(fill=tk.X, pady=(10, 0))

    def _build_period_tab(self):
        frame = ttk.Frame(self.tab_period, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)
        f1 = ttk.LabelFrame(frame, text=" Выбрать период ", padding=12)
        f1.pack(fill=tk.X, pady=6)
        ttk.Label(f1, text="С:").pack(side=tk.LEFT, padx=6)
        ttk.Entry(f1, textvariable=self.var_from, width=14).pack(side=tk.LEFT, padx=6)
        ttk.Label(f1, text="По:").pack(side=tk.LEFT, padx=6)
        ttk.Entry(f1, textvariable=self.var_to, width=14).pack(side=tk.LEFT, padx=6)
        ttk.Button(f1, text="Показать", command=self._show_period, style="Add.TButton").pack(side=tk.LEFT, padx=12)
        self.lbl_period_total = ttk.Label(f1, text="", font=("Segoe UI", 12, "bold"), foreground=self.FG_TITLE)
        self.lbl_period_total.pack(side=tk.LEFT, padx=20)
        f2 = ttk.LabelFrame(frame, text=" Расходы за период ", padding=10)
        f2.pack(fill=tk.BOTH, expand=True, pady=8)
        cols = ("amount", "category", "date", "note")
        self.tree_period = ttk.Treeview(f2, columns=cols, show="headings", selectmode="browse")
        self.tree_period.heading("amount", text="Сумма")
        self.tree_period.heading("category", text="Категория")
        self.tree_period.heading("date", text="Дата")
        self.tree_period.heading("note", text="Заметка")
        self.tree_period.column("amount", width=100)
        self.tree_period.column("category", width=130)
        self.tree_period.column("date", width=110)
        self.tree_period.column("note", width=300)
        self.tree_period.pack(fill=tk.BOTH, expand=True)

    def _refresh_all(self):
        for row in self.tree_exp.get_children():
            self.tree_exp.delete(row)
        for e in self.model.expenses:
            self.tree_exp.insert("", tk.END, values=(f"{e['amount']:.2f} руб.", e["category"], e["date"], e["note"]))
        total = self.model.get_total()
        self.lbl_total.config(text=f"Итого: {total:,.2f} руб.")
        self._draw_chart()
        self._show_summary_text()

    def _add_expense(self):
        try:
            amount = float(self.var_amount.get())
        except ValueError:
            messagebox.showwarning("Предупреждение", "Введите корректную сумму!")
            return
        if amount <= 0:
            messagebox.showwarning("Предупреждение", "Сумма должна быть положительной!")
            return
        self.model.add_expense(amount, self.var_category.get(), self.var_date.get(), self.var_note.get())
        self._refresh_all()
        self.model.save_to_file()
        self.var_amount.set("")
        self.var_note.set("")

    def _delete_expense(self):
        sel = self.tree_exp.selection()
        if not sel:
            messagebox.showwarning("Предупреждение", "Выберите расход!")
            return
        values = self.tree_exp.item(sel[0], "values")
        for i, e in enumerate(self.model.expenses):
            if f"{e['amount']:.2f} руб." == values[0] and e["category"] == values[1] and e["date"] == values[2]:
                self.model.delete_expense(i)
                break
        self._refresh_all()
        self.model.save_to_file()

    def _draw_chart(self):
        self.canvas.delete("all")
        data = self.model.get_by_category()
        if not data:
            return
        self.canvas.update_idletasks()
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 300
        max_val = max(v for _, v in data)
        if max_val == 0:
            return
        n = len(data)
        gap = 10
        bar_w = max(50, (w - 40) // n - gap)
        x = 10
        for cat, val in data:
            bar_h = (val / max_val) * (h - 80)
            color = self.CAT_COLORS.get(cat, "#7c5cbf")
            self.canvas.create_rectangle(x, h - 40 - bar_h, x + bar_w, h - 40, fill=color, outline="")
            self.canvas.create_text(x + bar_w // 2, h - 40 - bar_h - 12, text=f"{val:,.0f}", font=("Segoe UI", 8, "bold"), fill=self.FG_TITLE)
            self.canvas.create_text(x + bar_w // 2, h - 20, text=cat, font=("Segoe UI", 7), fill=self.FG_TEXT)
            x += bar_w + gap

    def _show_summary_text(self):
        self.text_summary.delete("1.0", tk.END)
        data = self.model.get_by_category()
        total = sum(v for _, v in data)
        if not data:
            self.text_summary.insert("1.0", "Нет данных.\n")
            return
        lines = [f"{'Категория':<20} {'Сумма':>10}  {'Доля':>8}", f"{'─'*42}"]
        for cat, val in data:
            pct = (val / total * 100) if total > 0 else 0
            lines.append(f"{cat:<20} {val:>10,.2f}  {pct:>6.1f}%")
        lines.append(f"{'─'*42}")
        lines.append(f"{'ИТОГО':<20} {total:>10,.2f}  {'100.0%':>6}")
        self.text_summary.insert("1.0", "\n".join(lines))

    def _show_period(self):
        for row in self.tree_period.get_children():
            self.tree_period.delete(row)
        date_from = self.var_from.get().strip()
        date_to = self.var_to.get().strip()
        if not date_from or not date_to:
            messagebox.showwarning("Предупреждение", "Введите даты!")
            return
        result = self.model.get_by_period(date_from, date_to)
        for e in result:
            self.tree_period.insert("", tk.END, values=(f"{e['amount']:.2f} руб.", e["category"], e["date"], e["note"]))
        total = self.model.get_total(result)
        self.lbl_period_total.config(text=f"Итого за период: {total:,.2f} руб.")

    def _export(self):
        fn = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialfile="expenses_export.json")
        if fn:
            self.model.save_to_file(fn)
            messagebox.showinfo("Успех", f"Экспортировано в {fn}")

    def _import(self):
        fn = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if fn:
            self.model.load_from_file(fn)
            self._refresh_all()
            messagebox.showinfo("Успех", f"Импортировано из {fn}")

    def _about(self):
        messagebox.showinfo("О программе", "Планировщик расходов v1.0\n\nЛабораторная работа №3\nДобавление трат, визуализация по категориям, итоги за период.")

    def _on_close(self):
        self.model.save_to_file()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetGUI(root)
    root.mainloop()