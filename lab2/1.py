import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTabWidget, QMessageBox

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt6 Tasks')
        self.setGeometry(200, 200, 400, 300)

        # Создаем вкладки
        tabs = QTabWidget()
        tabs.addTab(self.create_task1_ui(), "Task 1")
        tabs.addTab(self.create_task2_ui(), "Task 2")
        tabs.addTab(self.create_task3_ui(), "Task 3")

        # Основной layout
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

    def create_task1_ui(self):
        """Создание интерфейса для задания 1"""
        widget = QWidget()
        layout = QVBoxLayout()

        self.button = QPushButton('Нажми меня')
        self.label = QLabel('Отпущена')
        self.button.setCheckable(True)
        self.button.clicked.connect(self.update_button_state)

        layout.addWidget(self.button)
        layout.addWidget(self.label)
        widget.setLayout(layout)
        return widget

    def update_button_state(self):
        """Обновление состояния кнопки для задания 1"""
        if self.button.isChecked():
            self.label.setText('Нажата')
        else:
            self.label.setText('Отпущена')

    def create_task2_ui(self):
        """Создание интерфейса для задания 2"""
        widget = QWidget()
        layout = QVBoxLayout()

        self.counter = 0
        self.counter_label = QLabel('0')
        btn_increase = QPushButton('Увеличить на 1')
        btn_reset = QPushButton('Сбросить')

        btn_increase.clicked.connect(self.increase_counter)
        btn_reset.clicked.connect(self.reset_counter)

        layout.addWidget(self.counter_label)
        layout.addWidget(btn_increase)
        layout.addWidget(btn_reset)
        widget.setLayout(layout)
        return widget

    def increase_counter(self):
        """Увеличение счетчика для задания 2"""
        self.counter += 1
        self.counter_label.setText(str(self.counter))

    def reset_counter(self):
        """Сброс счетчика для задания 2"""
        self.counter = 0
        self.counter_label.setText(str(self.counter))

    def create_task3_ui(self):
        """Создание интерфейса для задания 3"""
        widget = QWidget()
        layout = QVBoxLayout()

        self.num1 = QLineEdit()
        self.num2 = QLineEdit()
        self.result_label = QLabel('Результат: ')
        self.calculate_btn = QPushButton('Вычислить')
        self.power_btn = QPushButton('Возвести в степень')

        self.num1.setPlaceholderText('Введите первое число')
        self.num2.setPlaceholderText('Введите второе число')

        self.calculate_btn.clicked.connect(self.calculate)
        self.power_btn.clicked.connect(self.calculate_power)

        layout.addWidget(self.num1)
        layout.addWidget(self.num2)
        layout.addWidget(self.calculate_btn)
        layout.addWidget(self.power_btn)
        layout.addWidget(self.result_label)
        widget.setLayout(layout)
        return widget

    def calculate(self):
        """Вычисление арифметических операций для задания 3"""
        try:
            num1 = int(self.num1.text())
            num2 = int(self.num2.text())
            result = num1 + num2
            self.result_label.setText(f'{num1} + {num2} = {result}')
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите целые числа.')

    def calculate_power(self):
        """Вычисление степени для задания 3"""
        try:
            num1 = int(self.num1.text())
            num2 = int(self.num2.text())
            result = num1 ** num2
            self.result_label.setText(f'{num1}<sup>{num2}</sup> = {result}')
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите целые числа.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())