from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox,
    QDialogButtonBox, QPushButton, QFileDialog
)
import json


class StartDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки игры")
        self.layout = QVBoxLayout(self)

        self.stone_spin = QSpinBox()
        self.stone_spin.setRange(5, 100)
        self.stone_spin.setValue(20)
        self.layout.addWidget(QLabel("Количество камней:"))
        self.layout.addWidget(self.stone_spin)

        self.mode_box = QComboBox()
        self.mode_box.addItems(["PvsAI", "PvsP"])
        self.layout.addWidget(QLabel("Режим игры:"))
        self.layout.addWidget(self.mode_box)

        self.win_box = QComboBox()
        self.win_box.addItems(["Взять последний", "Оставить последний"])
        self.layout.addWidget(QLabel("Условие победы:"))
        self.layout.addWidget(self.win_box)

        self.load_button = QPushButton("Загрузить игру")
        self.load_button.clicked.connect(self.load_game)
        self.layout.addWidget(self.load_button)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.result = None  # ('new', (stones, mode, win)) or ('load', path)

    def load_game(self):
        path, _ = QFileDialog.getOpenFileName(self, "Загрузить игру", "", "JSON Files (*.json)")
        if path:
            self.result = ('load', path)
            self.accept()

    def accept(self):
        if self.result is None:
            # Пользователь выбрал "OK", значит — новая игра
            self.result = ('new', (
                self.stone_spin.value(),
                self.mode_box.currentText(),
                self.win_box.currentText()
            ))
        super().accept()
