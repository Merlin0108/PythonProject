from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox

class AddEditDialog(QDialog):
    def __init__(self, parent=None, initial_value=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить / Редактировать число")
        self.value = None

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Введите целое число:")
        self.layout.addWidget(self.label)

        self.line_edit = QLineEdit(self)
        if initial_value is not None:
            self.line_edit.setText(str(initial_value))
        self.layout.addWidget(self.line_edit)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.accept_data)
        self.layout.addWidget(self.btn_ok)

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        self.layout.addWidget(self.btn_cancel)

    def accept_data(self):
        text = self.line_edit.text().strip()
        if self._is_valid_int(text):
            self.value = int(text)
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка ввода", "Введите корректное целое число.")

    def _is_valid_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
