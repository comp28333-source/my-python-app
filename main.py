import calendar
from datetime import datetime, date
import json
import os
import tkinter as tk
from tkinter import messagebox, filedialog

# Имя файла для сохранения заметок по умолчанию
NOTES_FILE = "notes.json"

# Словарь для русификации месяцев (все заглавными)
RUSSIAN_MONTHS = {
    1: "ЯНВАРЬ",
    2: "ФЕВРАЛЬ",
    3: "МАРТ",
    4: "АПРЕЛЬ",
    5: "МАЙ",
    6: "ИЮНЬ",
    7: "ИЮЛЬ",
    8: "АВГУСТ",
    9: "СЕНТЯБРЬ",
    10: "ОКТЯБРЬ",
    11: "НОЯБРЬ",
    12: "ДЕКАБРЬ",
}

MONTH_NAMES_LIST = [RUSSIAN_MONTHS[i] for i in range(1, 13)]

# Расширенная цветовая палитра (11 цветов)
DOT_COLORS = [
    "#00E676",  # Зеленый
    "#29B6F6",  # Синий
    "#EF5350",  # Красный
    "#FFEE58",  # Желтый
    "#AB47BC",  # Фиолетовый
    "#FFA726",  # Оранжевый
    "#26A69A",  # Бирюзовый
    "#EC407A",  # Розовый
    "#8D6E63",  # Коричневый
    "#78909C",  # Серо-синий
    "#FF7043",  # Коралловый
]


class CalendarApp:

  def __init__(self, root):
    self.root = root
    self.root.title(" КАЛЕНДАРЬ С ЗАМЕТКАМИ ")
    self.root.configure(bg="#f0f0f0")

    # Адаптивность главного окна
    self.root.rowconfigure(0, weight=0)  # Шапка навигации
    self.root.rowconfigure(1, weight=1)  # Сетка календаря
    self.root.rowconfigure(2, weight=0)  # Панель кнопок
    self.root.rowconfigure(3, weight=0)  # Панель подсчета
    self.root.columnconfigure(0, weight=1)

    # Загрузка заметок из файла
    self.notes = self.load_notes(NOTES_FILE)

    # Текущие данные для календаря
    now = datetime.now()
    self.today_year = now.year
    self.today_month = now.month
    self.today_day = now.day

    self.year = now.year
    self.month = now.month

    # ВЕРХНЯЯ ПАНЕЛЬ НАВИГАЦИИ (АДАПТИВНАЯ СЕТКА)
    self.nav_frame = tk.Frame(root, bg="#f0f0f0")
    self.nav_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=5)
    self.nav_frame.columnconfigure(0, weight=1)
    self.nav_frame.columnconfigure(1, weight=0)

    # Центрированный блок переключения месяцев (с адаптивным названием)
    center_nav = tk.Frame(self.nav_frame, bg="#f0f0f0")
    center_nav.grid(row=0, column=0, sticky="ew")
    center_nav.columnconfigure(1, weight=1)

    self.btn_prev = tk.Button(
        center_nav,
        text="<",
        font=("Arial", 11, "bold"),
        command=self.prev_month,
        bg="#e0e0e0",
        relief="raised",
        width=2,
    )
    self.btn_prev.grid(row=0, column=0, padx=2)

    self.header_label = tk.Label(
        center_nav,
        text="",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        fg="#222222",
        anchor="center",
    )
    self.header_label.grid(row=0, column=1, sticky="ew", padx=2)

    self.btn_next = tk.Button(
        center_nav,
        text=">",
        font=("Arial", 11, "bold"),
        command=self.next_month,
        bg="#e0e0e0",
        relief="raised",
        width=2,
    )
    self.btn_next.grid(row=0, column=2, padx=2)

    # Кнопка закрытия приложения
    btn_close_app = tk.Button(
        self.nav_frame,
        text="✕",
        font=("Arial", 11, "bold"),
        command=root.destroy,
        bg="#D32F2F",
        fg="white",
        relief="raised",
        width=2,
    )
    btn_close_app.grid(row=0, column=1, padx=(5, 0), sticky="e")

    # ГЛАВНЫЙ ФРЕЙМ СЕТКИ КАЛЕНДАРЯ (ВЫПУКЛЫЙ 3D-ЭФФЕКТ)
    self.frame = tk.Frame(root, bg="#d0d0d0", relief="raised", bd=3)
    self.frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=2)

    for i in range(7):
      self.frame.columnconfigure(i, weight=1)
    for i in range(7):
      self.frame.rowconfigure(i, weight=1)

    self.create_file_control_panel()
    self.create_counter_panel()
    self.update_calendar()

  def load_notes(self, filepath):
    if os.path.exists(filepath):
      try:
        with open(filepath, "r", encoding="utf-8") as f:
          data = json.load(f)
          formatted = {}
          for k, v in data.items():
            if isinstance(v, str):
              formatted[k] = {"text": v, "color": "#00E676"}
            else:
              formatted[k] = v
          return formatted
      except Exception:
        return {}
    return {}

  def save_notes(self):
    try:
      with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(self.notes, f, ensure_ascii=False, indent=4)
    except Exception as e:
      messagebox.showerror(
          "ОШИБКА", f"НЕ УДАЛОСЬ СОХРАНИТЬ ЗАМЕТКУ В ФАЙЛ:\n{e}"
      )

  def prev_month(self):
    self.month -= 1
    if self.month < 1:
      self.month = 12
      self.year -= 1
    self.update_calendar()

  def next_month(self):
    self.month += 1
    if self.month > 12:
      self.month = 1
      self.year += 1
    self.update_calendar()

  def create_file_control_panel(self):
    ctrl_frame = tk.Frame(self.root, bg="#f0f0f0")
    ctrl_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=2)
    ctrl_frame.columnconfigure(0, weight=1)
    ctrl_frame.columnconfigure(1, weight=1)
    ctrl_frame.columnconfigure(2, weight=1)

    btn_export = tk.Button(
        ctrl_frame,
        text="ЭКСПОРТ",
        font=("Arial", 9, "bold"),
        bg="#455A64",
        fg="white",
        command=self.export_notes,
    )
    btn_export.grid(row=0, column=0, sticky="ew", padx=2)

    btn_import = tk.Button(
        ctrl_frame,
        text="ИМПОРТ",
        font=("Arial", 9, "bold"),
        bg="#455A64",
        fg="white",
        command=self.import_notes,
    )
    btn_import.grid(row=0, column=1, sticky="ew", padx=2)

    btn_clear = tk.Button(
        ctrl_frame,
        text="ОЧИСТИТЬ",
        font=("Arial", 9, "bold"),
        bg="#C62828",
        fg="white",
        command=self.clear_current_month,
    )
    btn_clear.grid(row=0, column=2, sticky="ew", padx=2)

  def export_notes(self):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("JSON ФАЙЛЫ", "*.json"), ("ВСЕ ФАЙЛЫ", "*.*")],
        title="СОХРАНИТЬ ЗАМЕТКИ КАК...",
    )
    if file_path:
      try:
        with open(file_path, "w", encoding="utf-8") as f:
          json.dump(self.notes, f, ensure_ascii=False, indent=4)
        messagebox.showinfo(
            "УСПЕХ", f"ЗАМЕТКИ УСПЕШНО ЭКСПОРТИРОВАНЫ В:\n{file_path}"
        )
      except Exception as e:
        messagebox.showerror("ОШИБКА", f"НЕ УДАЛОСЬ ЭКСПОРТИРОВАТЬ ФАЙЛ:\n{e}")

  def import_notes(self):
    file_path = filedialog.askopenfilename(
        filetypes=[("JSON ФАЙЛЫ", "*.json"), ("ВСЕ ФАЙЛЫ", "*.*")],
        title="ВЫБЕРИТЕ ФАЙЛ С ЗАМЕТКАМИ",
    )
    if file_path:
      imported_data = self.load_notes(file_path)
      if imported_data:
        self.notes.update(imported_data)
        self.save_notes()
        self.update_calendar()
        messagebox.showinfo("УСПЕХ", "ЗАМЕТКИ УСПЕШНО ИМПОРТИРОВАНЫ И ЗАГРУЖЕНЫ!")
      else:
        messagebox.showwarning(
            "ВНИМАНИЕ", "ФАЙЛ ПУСТ ИЛИ ИМЕЕТ НЕВЕРНЫЙ ФОРМАТ."
        )

  def clear_current_month(self):
    month_name = RUSSIAN_MONTHS[self.month]
    if not messagebox.askyesno(
        "ПОДТВЕРЖДЕНИЕ",
        f"ВЫ ДЕЙСТВИТЕЛЬНО ХОТИТЕ УДАЛИТЬ ВСЕ ЗАМЕТКИ ЗА {month_name}"
        f" {self.year} ГОДА?",
    ):
      return
    keys_to_delete = [
        k
        for k in self.notes.keys()
        if k.startswith(f"{self.year:04d}-{self.month:02d}-")
    ]
    for k in keys_to_delete:
      del self.notes[k]
    self.save_notes()
    self.update_calendar()
    messagebox.showinfo("ГОТОВО", f"ВСЕ ЗАМЕТКИ ЗА {month_name} УДАЛЕНЫ.")

  def create_counter_panel(self):
    counter_frame = tk.LabelFrame(
        self.root,
        text="ЗА ПЕРИОД:",
        font=("Arial", 9, "bold"),
        bg="#f0f0f0",
        fg="#333333",
    )
    counter_frame.grid(row=3, column=0, sticky="ew", padx=8, pady=(2, 6))

    row_from = tk.Frame(counter_frame, bg="#f0f0f0")
    row_from.pack(fill="x", padx=4, pady=1)
    tk.Label(
        row_from,
        text="С:",
        font=("Arial", 9, "bold"),
        bg="#f0f0f0",
        width=3,
        anchor="w",
    ).pack(side="left")
    self.from_day_var = tk.IntVar(value=1)
    tk.Spinbox(
        row_from,
        from_=1,
        to=31,
        textvariable=self.from_day_var,
        font=("Arial", 9, "bold"),
        width=3,
    ).pack(side="left", padx=1)
    self.from_month_var = tk.StringVar(value=RUSSIAN_MONTHS[self.today_month])
    tk.OptionMenu(row_from, self.from_month_var, *MONTH_NAMES_LIST).pack(
        side="left", padx=2
    )
    self.from_year_var = tk.IntVar(value=self.today_year)
    tk.Spinbox(
        row_from,
        from_=2000,
        to=2100,
        textvariable=self.from_year_var,
        font=("Arial", 9, "bold"),
        width=4,
    ).pack(side="left", padx=1)

    row_to = tk.Frame(counter_frame, bg="#f0f0f0")
    row_to.pack(fill="x", padx=4, pady=1)
    tk.Label(
        row_to,
        text="ПО:",
        font=("Arial", 9, "bold"),
        bg="#f0f0f0",
        width=3,
        anchor="w",
    ).pack(side="left")
    self.to_day_var = tk.IntVar(value=self.today_day)
    tk.Spinbox(
        row_to,
        from_=1,
        to=31,
        textvariable=self.to_day_var,
        font=("Arial", 9, "bold"),
        width=3,
    ).pack(side="left", padx=1)
    self.to_month_var = tk.StringVar(value=RUSSIAN_MONTHS[self.today_month])
    tk.OptionMenu(row_to, self.to_month_var, *MONTH_NAMES_LIST).pack(
        side="left", padx=2
    )
    self.to_year_var = tk.IntVar(value=self.today_year)
    tk.Spinbox(
        row_to,
        from_=2000,
        to=2100,
        textvariable=self.to_year_var,
        font=("Arial", 9, "bold"),
        width=4,
    ).pack(side="left", padx=1)

    row_btn = tk.Frame(counter_frame, bg="#f0f0f0")
    row_btn.pack(fill="x", padx=4, pady=2)
    btn_calc = tk.Button(
        row_btn,
        text="ПОСЧИТАТЬ",
        font=("Arial", 9, "bold"),
        bg="#1976D2",
        fg="white",
        command=self.calculate_notes,
    )
    btn_calc.pack(side="left", padx=1)

    btn_set_today = tk.Button(
        row_btn,
        text="НА СЕГОДНЯ",
        font=("Arial", 8, "bold"),
        bg="#607D8B",
        fg="white",
        command=self.set_to_today,
    )
    btn_set_today.pack(side="left", padx=2)

    res_container = tk.Frame(row_btn, bg="#f0f0f0")
    res_container.pack(side="right", padx=2)
    self.res_title_lbl = tk.Label(
        res_container,
        text="ВСЕГО: ",
        font=("Arial", 9, "bold"),
        bg="#f0f0f0",
        fg="#D32F2F",
    )
    self.res_title_lbl.pack(side="left")
    self.res_num_lbl = tk.Label(
        res_container,
        text="0",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        fg="#D32F2F",
    )
    self.res_num_lbl.pack(side="left")
    self.res_desc_lbl = tk.Label(
        res_container,
        text=" ДНЕЙ.",
        font=("Arial", 9, "bold"),
        bg="#f0f0f0",
        fg="#D32F2F",
    )
    self.res_desc_lbl.pack(side="left")

  def set_to_today(self):
    now = datetime.now()
    self.to_day_var.set(now.day)
    self.to_month_var.set(RUSSIAN_MONTHS[now.month])
    self.to_year_var.set(now.year)
    self.calculate_notes()

  def calculate_notes(self):
    try:
      d1, m1_name, y1 = (
          self.from_day_var.get(),
          self.from_month_var.get(),
          self.from_year_var.get(),
      )
      d2, m2_name, y2 = (
          self.to_day_var.get(),
          self.to_month_var.get(),
          self.to_year_var.get(),
      )
      m1 = MONTH_NAMES_LIST.index(m1_name) + 1
      m2 = MONTH_NAMES_LIST.index(m2_name) + 1
      start_date, end_date = date(y1, m1, d1), date(y2, m2, d2)
    except Exception as e:
      messagebox.showerror(
          "ОШИБКА", f"ПРОВЕРЬТЕ ПРАВИЛЬНОСТЬ ВВЕДЕННЫХ ДАТ:\n{e}"
      )
      return

    if start_date > end_date:
      messagebox.showerror(
          "ОШИБКА", "ДАТА 'С' НЕ МОЖЕТ БЫТЬ ПОЗЖЕ ДАТЫ 'ПО'!"
      )
      return

    count = 0
    for date_str, note_info in self.notes.items():
      note_text = (
          note_info.get("text", "")
          if isinstance(note_info, dict)
          else str(note_info)
      )
      if note_text.strip():
        try:
          note_date = datetime.strptime(date_str, "%Y-%m-%d").date()
          if start_date <= note_date <= end_date:
            count += 1
        except Exception:
          pass
    self.res_num_lbl.config(text=str(count))

  def on_day_click(self, y, m, d):
    date_str = f"{y:04d}-{m:02d}-{d:02d}"
    note_data = self.notes.get(date_str, {})
    if isinstance(note_data, str):
      current_note, current_color_hex = note_data, "#00E676"
    else:
      current_note = note_data.get("text", "")
      current_color_hex = note_data.get("color", "#00E676")

    # КОМПАКТНОЕ И УЗКОЕ ОКНО ЗАМЕТКИ
    note_window = tk.Toplevel(self.root)
    note_window.title(f"ЗАМЕТКА: {d} {RUSSIAN_MONTHS[m]} {y}")
    note_window.configure(bg="#f0f0f0")
    note_window.grab_set()

    note_window.rowconfigure(2, weight=1)
    note_window.columnconfigure(0, weight=1)

    lbl = tk.Label(
        note_window,
        text=f"ЗАМЕТКА НА {date_str}:",
        font=("Arial", 9, "bold"),
        bg="#f0f0f0",
        fg="#333333",
    )
    lbl.grid(row=0, column=0, sticky="w", padx=8, pady=(6, 2))

    # Палитра цветов (компактная сетка в 2 ряда)
    color_frame = tk.LabelFrame(
        note_window,
        text="ЦВЕТ ТОЧКИ",
        font=("Arial", 8, "bold"),
        bg="#f0f0f0",
        fg="#333333",
    )
    color_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=2)

    palette_container = tk.Frame(color_frame, bg="#f0f0f0")
    palette_container.pack(padx=2, pady=3)

    selected_color = {"hex": current_color_hex}
    color_buttons = []

    def select_color(hex_val, btn):
      selected_color["hex"] = hex_val
      for b in color_buttons:
        b.config(relief="raised", bd=2)
      btn.config(relief="sunken", bd=2)

    row1_frame = tk.Frame(palette_container, bg="#f0f0f0")
    row1_frame.pack(anchor="w", pady=1)
    row2_frame = tk.Frame(palette_container, bg="#f0f0f0")
    row2_frame.pack(anchor="w", pady=1)

    for idx, hex_val in enumerate(DOT_COLORS):
      target_parent = row1_frame if idx < 6 else row2_frame
      btn = tk.Button(
          target_parent,
          bg=hex_val,
          width=2,
          height=1,
          relief="raised",
          bd=1,
      )
      btn.config(command=lambda h=hex_val, b=btn: select_color(h, b))
      btn.pack(side="left", padx=1)
      color_buttons.append(btn)
      if hex_val == current_color_hex:
        btn.config(relief="sunken", bd=2)

    text_box = tk.Text(
        note_window, font=("Arial", 10, "bold"), width=14, height=4
    )
    text_box.grid(row=2, column=0, sticky="nsew", padx=8, pady=3)
    text_box.insert("1.0", current_note)

    def save_and_close():
      new_note = text_box.get("1.0", "end-1c").strip()
      chosen_color_hex = selected_color["hex"]
      if new_note:
        self.notes[date_str] = {"text": new_note, "color": chosen_color_hex}
      else:
        if date_str in self.notes:
          del self.notes[date_str]
      self.save_notes()
      note_window.destroy()
      self.update_calendar()

    btn_save = tk.Button(
        note_window,
        text="СОХРАНИТЬ",
        font=("Arial", 10, "bold"),
        bg="#2E7D32",
        fg="white",
        activebackground="#43A047",
        activeforeground="white",
        command=save_and_close,
        height=1,
    )
    btn_save.grid(row=3, column=0, sticky="ew", padx=8, pady=(2, 8))

    note_window.update_idletasks()
    note_window.minsize(200, 240)

  def update_calendar(self):
    for widget in self.frame.winfo_children():
      widget.destroy()

    month_name = RUSSIAN_MONTHS[self.month]
    self.header_label.config(text=f"{month_name} {self.year}")

    days_of_week = ["ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС"]
    for col, day_name in enumerate(days_of_week):
      # Дни недели жирным шрифтом и в стиле объемных кнопок
      lbl = tk.Label(
          self.frame,
          text=day_name,
          font=("Arial", 12, "bold"),
          bg="#cfd8dc",
          fg="#1a237e",
          relief="raised",
          bd=2,
      )
      lbl.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

    cal = calendar.Calendar(firstweekday=0)
    month_days = list(cal.itermonthdays3(self.year, self.month))

    for idx, (y, m, d) in enumerate(month_days):
      row_idx = idx // 7 + 1
      col_idx = idx % 7

      date_str = f"{y:04d}-{m:02d}-{d:02d}"
      note_info = self.notes.get(date_str, None)

      has_note = False
      dot_color = "#00E676"

      if note_info:
        if isinstance(note_info, dict):
          if note_info.get("text", "").strip():
            has_note = True
            dot_color = note_info.get("color", "#00E676")
        elif isinstance(note_info, str) and note_info.strip():
          has_note = True

      is_today = (
          d == self.today_day and m == self.today_month and y == self.today_year
      )
      is_current_month = m == self.month

      if is_current_month:
        fg_color = "#000000"
        bg_day = "#F8C1C0" if is_today else "#ffffff"
      else:
        fg_color = "#777777"
        bg_day = "#e8e8e8"

      # Выпуклые 3D границы для ячеек дней
      day_frame = tk.Frame(self.frame, bg="#d0d0d0", relief="raised", bd=1)
      day_frame.grid(
          row=row_idx, column=col_idx, sticky="nsew", padx=1, pady=1
      )

      inner_frame = tk.Frame(day_frame, bg=bg_day)
      inner_frame.pack(fill="both", expand=True)

      day_lbl = tk.Label(
          inner_frame,
          text=str(d),
          font=("Arial", 11, "bold"),
          bg=bg_day,
          fg=fg_color,
      )
      day_lbl.place(relx=0.5, rely=0.28, anchor="center")

      if has_note:
        ball_canvas = tk.Canvas(
            inner_frame,
            width=16,
            height=16,
            bg=bg_day,
            highlightthickness=0,
            bd=0,
        )
        ball_canvas.place(relx=0.5, rely=0.78, anchor="center")
        ball_canvas.create_oval(
            1,
            1,
            15,
            15,
            fill=dot_color,
            outline="#333333",
            width=1,
        )

      for widget in (day_frame, inner_frame, day_lbl):
        widget.bind(
            "<Button-1>", lambda e, yy=y, mm=m, dd=d: self.on_day_click(yy, mm, dd)
        )


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry("360x640")  # Компактный старт под мобильные экраны
  app = CalendarApp(root)
  root.mainloop()
