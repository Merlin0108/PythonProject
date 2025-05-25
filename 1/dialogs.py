from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QComboBox, QDialogButtonBox, QFileDialog
)


class NewGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новая игра")
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

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

    def get_settings(self):
        return self.stone_spin.value(), self.mode_box.currentText(), self.win_box.currentText()
