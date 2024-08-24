import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class FileExplorer:
    def __init__(self, root):
        """
        Инициализация главного окна и настройка основных параметров.
        """
        self.root = root
        self.root.title("File Explorer")
        self.root.geometry("800x600")

        # Начальный путь - домашняя директория пользователя
        self.current_path = os.path.expanduser("~")

        # Создание виджетов
        self.create_widgets()

    def create_widgets(self):
        """
        Создание всех виджетов и их размещение в окне.
        """
        self.create_toolbar()

        # Создание и настройка Treeview для отображения файлов и папок
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Привязка двойного щелчка к методу on_double_click
        self.tree.bind("<Double-1>", self.on_double_click)

        # Заполнение Treeview начальным путем
        self.populate_tree(self.current_path)

    def create_toolbar(self):
        """
        Создание панели инструментов с кнопками.
        """
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill=tk.X)

        # Кнопка открытия файла
        btn_open = ttk.Button(toolbar, text="Open", command=self.open_file)
        btn_open.pack(side=tk.LEFT)

        # Кнопка обновления
        btn_refresh = ttk.Button(toolbar, text="Refresh", command=self.refresh)
        btn_refresh.pack(side=tk.LEFT)

        # Кнопка переключения темы
        btn_view = ttk.Button(toolbar, text="View", command=self.toggle_theme)
        btn_view.pack(side=tk.LEFT)

        # Переменная для хранения текущей темы
        self.theme_var = tk.StringVar(value="light")

    def populate_tree(self, path):
        """
        Заполнение Treeview содержимым указанного пути.
        """
        # Очистка текущего содержимого Treeview
        self.tree.delete(*self.tree.get_children())

        # Вставка корневого элемента с указанным путем
        parent = self.tree.insert("", "end", text=path, open=True)

        # Вставка элементов в Treeview
        self.insert_items(parent, path)

    def insert_items(self, parent, path):
        """
        Рекурсивная вставка элементов в Treeview.
        """
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                # Вставка папки
                oid = self.tree.insert(parent, "end", text=item, values=[item_path])
                self.tree.insert(oid, "end", text="dummy")
            else:
                # Вставка файла
                self.tree.insert(parent, "end", text=item, values=[item_path])

    def on_double_click(self, event):
        """
        Обработка двойного щелчка на элементе Treeview.
        """
        item = self.tree.selection()[0]
        item_path = self.tree.item(item, "values")[0]
        if os.path.isdir(item_path):
            # Если элемент - папка, обновить Treeview
            self.populate_tree(item_path)
        else:
            # Если элемент - файл, открыть его
            self.open_file(item_path)

    def open_file(self, file_path=None):
        """
        Открытие файла с помощью системного средства просмотра.
        """
        if file_path is None:
            file_path = filedialog.askopenfilename(initialdir=self.current_path)
        if file_path:
            if os.path.isfile(file_path):
                os.system(f"xdg-open '{file_path}'")
            else:
                messagebox.showerror("Error", "Selected item is not a file.")

    def refresh(self):
        """
        Обновление содержимого Treeview.
        """
        self.populate_tree(self.current_path)

    def toggle_theme(self):
        """
        Переключение между светлой и темной темами.
        """
        current_theme = self.theme_var.get()
        if current_theme == "light":
            self.apply_dark_theme()
            self.theme_var.set("dark")
        else:
            self.apply_light_theme()
            self.theme_var.set("light")

    def apply_dark_theme(self):
        """
        Применение темной темы.
        """
        self.root.tk_setPalette(background='#333333', foreground='white')
        self.tree.config(style="Treeview")
        style = ttk.Style()
        style.configure("Treeview", background="#555555", foreground="white", fieldbackground="#555555")
        style.map("Treeview", background=[('selected', '#777777')], foreground=[('selected', 'white')])

    def apply_light_theme(self):
        """
        Применение светлой темы.
        """
        self.root.tk_setPalette(background='white', foreground='black')
        self.tree.config(style="Treeview")
        style = ttk.Style()
        style.configure("Treeview", background="white", foreground="black", fieldbackground="white")
        style.map("Treeview", background=[('selected', '#add8e6')], foreground=[('selected', 'black')])

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()