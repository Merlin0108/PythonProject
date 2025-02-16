import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from book import Book

class BookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 400, 600)
        self.setWindowTitle('Информация о книгах')

        # Создаем книги
        books = [
            Book("Война и мир", "Лев Толстой", 1225, "war_and_peace.jpg"),
            Book("1984", "Джордж Оруэлл", 328, "1984.jpg"),
            Book("Мастер и Маргарита", "Михаил Булгаков", 480, "master_and_margarita.jpg")
        ]

        # Создаем вертикальный layout
        layout = QVBoxLayout()

        for book in books:
            # Создаем виджет для каждой книги
            book_widget = QWidget()
            book_layout = QVBoxLayout()

            # Добавляем информацию о книге
            info_label = QLabel(book.get_info())
            info_label.setFont(QFont('Arial', 12))
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            book_layout.addWidget(info_label)

            # Добавляем обложку
            cover_label = QLabel()
            try:
                pixmap = QPixmap(book.cover_path)
                if pixmap.isNull():
                    raise FileNotFoundError("Обложка не найдена.")
                cover_label.setPixmap(pixmap.scaled(200, 300, Qt.AspectRatioMode.KeepAspectRatio))
                cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                cover_label.setText(f"Ошибка загрузки обложки: {e}")
            book_layout.addWidget(cover_label)

            book_widget.setLayout(book_layout)
            layout.addWidget(book_widget)

        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BookApp()
    window.show()
    sys.exit(app.exec())