import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTreeView, QVBoxLayout,
                             QPushButton, QFileSystemModel, QInputDialog,
                             QMessageBox)
from PyQt5.QtCore import QDir, QFileInfo


class FileManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File System Manager')
        self.setGeometry(300, 300, 800, 600)

        # Создание модели файловой системы
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.homePath())
        self.model.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot | QDir.AllDirs)

        # Настройка дерева для отображения
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))

        # Кнопки управления
        self.btn_add = QPushButton('Добавить каталог')
        self.btn_add.clicked.connect(self.add_directory)

        self.btn_del = QPushButton('Удалить каталог')
        self.btn_del.clicked.connect(self.delete_directory)

        # Компоновка интерфейса
        layout = QVBoxLayout()
        layout.addWidget(self.tree)
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_del)

        self.setLayout(layout)

    def add_directory(self):
        # Получение текущего выбранного пути
        index = self.tree.currentIndex()
        path = self.model.filePath(index) if index.isValid() else QDir.homePath()

        # Диалог ввода имени новой папки
        name, ok = QInputDialog.getText(self, 'Создание каталога',
                                        'Введите имя нового каталога:')
        if ok and name:
            new_path = QDir(path).filePath(name)
            dir = QDir()

            # Попытка создания каталога
            if dir.mkdir(new_path):
                self.tree.expand(index)
            else:
                QMessageBox.warning(self, 'Ошибка',
                                    'Не удалось создать каталог! Проверьте права.')

    def delete_directory(self):
        # Получение выбранного элемента
        index = self.tree.currentIndex()
        if not index.isValid():
            return

        path = self.model.filePath(index)
        file_info = QFileInfo(path)

        # Проверка что это каталог
        if not file_info.isDir():
            QMessageBox.warning(self, 'Ошибка', 'Выберите каталог для удаления!')
            return

        # Подтверждение удаления
        reply = QMessageBox.question(self, 'Подтверждение',
                                     f'Удалить каталог "{file_info.fileName()}"?',
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            dir = QDir()
            # Сначала пробуем удалить пустой каталог
            if not dir.rmdir(path):
                # Если не получилось - рекурсивное удаление
                if dir.removeRecursively(path):
                    QMessageBox.information(self, 'Успех', 'Каталог удалён')
                else:
                    QMessageBox.warning(self, 'Ошибка',
                                        'Не удалось удалить каталог!')
            else:
                QMessageBox.information(self, 'Успех', 'Пустой каталог удалён')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileManagerApp()
    ex.show()
    sys.exit(app.exec_())