import os

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QAction, QFileDialog, QMessageBox, QInputDialog
)
from data_model import SequenceModel
from chart_view import ChartView
from text_view import TextView
from dialogs import AddEditDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sequence Analyzer")
        self.resize(800, 600)

        self.model = SequenceModel()

        self.chart_view = ChartView()
        self.text_view = TextView()

        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)

        self.chart_view.setStyleSheet("border: 2px solid #555; padding: 10px;")
        self.text_view.setStyleSheet("border: 2px solid #555; padding: 10px;")

        layout.addWidget(self.chart_view, 2)
        layout.addWidget(self.text_view, 1)
        self.setCentralWidget(central_widget)

        self._create_menu()

        # Путь к файлу с данными
        default_file = os.path.join(os.path.dirname(__file__), "data.txt")

        # Загружаем данные при старте, если файл существует
        if os.path.exists(default_file):
            try:
                self.model.load_from_file(default_file)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл при старте:\n{e}")

        self._update_views()

    def _create_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&Файл")
        load_action = QAction("&Загрузить", self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

        exit_action = QAction("Вы&ход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu("&Правка")
        add_action = QAction("&Добавить", self)
        add_action.triggered.connect(self.add_number)
        edit_menu.addAction(add_action)

        edit_action = QAction("&Редактировать", self)
        edit_action.triggered.connect(self.edit_number)
        edit_menu.addAction(edit_action)

        delete_action = QAction("&Удалить", self)
        delete_action.triggered.connect(self.delete_number)
        edit_menu.addAction(delete_action)

    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if filename:
            try:
                self.model.load_from_file(filename)
                self._update_views()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл:\n{e}")

    def add_number(self):
        dialog = AddEditDialog(self)
        if dialog.exec_():
            self.model.add_number(dialog.value)
            self._update_views()

    def edit_number(self):
        if not self.model.numbers:
            QMessageBox.information(self, "Информация", "Данные отсутствуют для редактирования.")
            return

        unique_numbers = list(sorted(set(self.model.numbers)))
        count = len(unique_numbers)

        idx, ok = QInputDialog.getInt(
            self,
            "Редактировать число",
            f"Выберите индекс уникального числа (1-{count}):\n{', '.join(f'{i + 1}: {val}' for i, val in enumerate(unique_numbers))}",
            min=1,
            max=count
        )
        if not ok:
            return

        number_to_edit = unique_numbers[idx - 1]

        occurrences = [i for i, num in enumerate(self.model.numbers) if num == number_to_edit]

        if len(occurrences) == 1:
            index_to_edit = occurrences[0]
        else:
            choice_str = "\n".join([f"{i + 1}: позиция {pos}" for i, pos in enumerate(occurrences)])
            choice, ok = QInputDialog.getInt(
                self,
                "Выбор вхождения",
                f"Число {number_to_edit} встречается в следующих позициях:\n{choice_str}\nВыберите номер вхождения для редактирования:",
                min=1,
                max=len(occurrences)
            )
            if not ok:
                return
            index_to_edit = occurrences[choice - 1]

        current_value = self.model.numbers[index_to_edit]
        dialog = AddEditDialog(self, initial_value=current_value)
        if dialog.exec_():
            self.model.edit_number(index_to_edit, dialog.value)
            self._update_views()

    def delete_number(self):
        if not self.model.numbers:
            QMessageBox.information(self, "Информация", "Данные отсутствуют для удаления.")
            return

        unique_numbers = list(sorted(set(self.model.numbers)))
        count = len(unique_numbers)

        idx, ok = QInputDialog.getInt(
            self,
            "Удалить число",
            f"Выберите индекс уникального числа для удаления (1-{count}):\n" +
            '\n'.join(f"{i + 1}: {val}" for i, val in enumerate(unique_numbers)),
            min=1,
            max=count
        )
        if not ok:
            return

        number_to_delete = unique_numbers[idx - 1]
        occurrences = [i for i, val in enumerate(self.model.numbers) if val == number_to_delete]

        if len(occurrences) == 1:
            # Удалить единственное вхождение
            self.model.delete_number(occurrences[0])
        else:
            choice, ok = QInputDialog.getItem(
                self,
                "Удалить вхождение",
                f"Число {number_to_delete} встречается {len(occurrences)} раз. Что удалить?",
                [f"Вхождение {i + 1} (позиция {pos + 1})" for i, pos in enumerate(occurrences)] + ["Удалить все"],
                editable=False
            )
            if not ok:
                return
            if choice == "Удалить все":
                for index in sorted(occurrences, reverse=True):
                    self.model.delete_number(index)
            else:
                chosen_index = int(choice.split()[1]) - 1
                self.model.delete_number(occurrences[chosen_index])

        self._update_views()

    def _update_views(self):
        freq = self.model.get_frequencies()
        minimum = self.model.get_min()
        maximum = self.model.get_max()
        mean = self.model.get_mean()
        mode = self.model.get_mode()

        self.chart_view.set_frequencies(freq)
        self.text_view.update_text(freq, minimum, maximum, mean, mode)
