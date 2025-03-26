import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QLabel, QDialog, QCheckBox)

class AgreementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agreement")
        layout = QVBoxLayout()
        self.checkbox = QCheckBox("Соглашаюсь")
        self.ok_button = QPushButton("OK")
        layout.addWidget(self.checkbox)
        layout.addWidget(self.ok_button)
        self.ok_button.clicked.connect(self.accept)
        self.setLayout(layout)

    def is_agreed(self):
        return self.checkbox.isChecked()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Главное окно")
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.button = QPushButton("Открыть диалог")
        self.label = QLabel("Состояние: Неизвестно")
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.button.clicked.connect(self.show_dialog)

    def show_dialog(self):
        dialog = AgreementDialog(self)
        if dialog.exec() == QDialog.Accepted:
            state = "Согласен" if dialog.is_agreed() else "Не согласен"
            self.label.setText(f"Состояние: {state}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())