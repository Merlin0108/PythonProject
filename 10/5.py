import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QTextEdit, QVBoxLayout, QFileDialog)
from PyQt5.QtCore import QFileInfo, QDateTime


class FileInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CSV File Information')
        self.setGeometry(300, 300, 500, 400)

        # Создание виджетов
        self.btn = QPushButton('Выбрать CSV файл', self)
        self.btn.clicked.connect(self.showDialog)

        self.text = QTextEdit(self)
        self.text.setReadOnly(True)

        # Настройка лейаута
        layout = QVBoxLayout()
        layout.addWidget(self.btn)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def showDialog(self):
        # Открытие диалога выбора файла с фильтром .csv
        fname, _ = QFileDialog.getOpenFileName(
            self, 'Выберите CSV файл', '',
            'CSV Files (*.csv)'
        )

        if fname:
            file_info = QFileInfo(fname)
            info = []

            # Сбор информации
            info.append(f"Абсолютный путь: {file_info.absoluteFilePath()}")
            info.append(f"Базовое имя: {file_info.baseName()}")
            info.append(f"Доступен для чтения: {file_info.isReadable()}")
            info.append(f"Доступен для записи: {file_info.isWritable()}")
            info.append(f"Исполняемый: {file_info.isExecutable()}")
            info.append(f"Дата создания: {file_info.birthTime().toString('dd.MM.yyyy HH:mm:ss')}")
            info.append(f"Последнее изменение: {file_info.lastModified().toString('dd.MM.yyyy HH:mm:ss')}")

            self.text.setText('\n'.join(info))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileInfoApp()
    ex.show()
    sys.exit(app.exec_())