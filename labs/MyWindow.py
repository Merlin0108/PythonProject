import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 1. Создаем квадратное окно
        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Графическое приложение')

        # 2. Создаем первую метку
        self.label1 = QLabel(self)
        self.label1.setText("Это длинный текст, который будет переноситься на следующую строку.")
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 3. Выравниваем текст по центру
        self.label1.setWordWrap(True)  # 4. Включаем перенос текста
        font1 = QFont('Arial', 10)  # Создаем шрифт
        font1.setItalic(True)  # 5. Делаем текст курсивным
        self.label1.setFont(font1)
        self.label1.setMargin(10)  # 7. Задаем внешние отступы

        # 6. Создаем вторую метку
        self.label2 = QLabel(self)
        self.label2.setText("Вторая метка")
        self.label2.move(50, 100)  # Смещаем метку ниже первой
        self.label2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)  # Выравниваем по центру и нижней части
        font2 = QFont('Arial', 20)  # Шрифт в два раза больше
        self.label2.setFont(font2)
        self.label2.setMargin(10)  # 7. Задаем внешние отступы

        # 8. Создаем третью метку с картинкой
        self.label3 = QLabel(self)
        self.label3.move(50, 200)
        try:
            pixmap = QPixmap("image.png")  # Загружаем картинку
            if pixmap.isNull():
                raise FileNotFoundError("Картинка не найдена или не может быть загружена.")
            self.label3.setPixmap(pixmap)
        except Exception as e:
            self.label3.setText(f"Ошибка: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())