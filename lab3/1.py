from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QCheckBox, QDoubleSpinBox, QHBoxLayout, QTextEdit, QDateEdit, QPushButton )
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
import sys


def get_season_info(season):
    info = {
        "Весна": "Весна - пора цветения и пробуждения природы.",
        "Лето": "Лето - тёплые дни и отпускное время.",
        "Осень": "Осень - время сбора урожая и золотых листьев.",
        "Зима": "Зима - снег, морозы и новогодние праздники."
    }
    return info.get(season, "")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Блок с временами года
        self.season_label = QLabel()
        self.season_group = QGroupBox("Выберите время года")
        season_layout = QVBoxLayout()
        self.season_buttons = {}
        default_season = "Весна"

        for season in ["Весна", "Лето", "Осень", "Зима"]:
            btn = QRadioButton(season)
            btn.toggled.connect(self.update_season_info)
            self.season_buttons[season] = btn
            season_layout.addWidget(btn)

        self.season_buttons[default_season].setChecked(True)
        self.update_season_info()

        self.season_group.setLayout(season_layout)
        layout.addWidget(self.season_group)
        layout.addWidget(self.season_label)

        # Блок с продуктами
        self.products = [
            ("Яблоки", 100),
            ("Молоко", 80),
            ("Хлеб", 50),
            ("Сыр", 200),
            ("Шоколад", 150)
        ]
        self.product_widgets = {}
        self.total_label = QLabel("Общая стоимость: 0 руб.")

        for name, price in self.products:
            hbox = QHBoxLayout()
            checkbox = QCheckBox(name)
            quantity = QDoubleSpinBox()
            quantity.setRange(0, 100)
            quantity.setSingleStep(1)
            quantity.setEnabled(False)
            checkbox.stateChanged.connect(lambda _, c=checkbox, q=quantity: self.toggle_product(c, q))
            quantity.valueChanged.connect(self.calculate_total)

            price_label = QLabel(f"Цена: {price} руб.")
            self.product_widgets[name] = (checkbox, quantity, price, price_label)
            hbox.addWidget(checkbox)
            hbox.addWidget(quantity)
            hbox.addWidget(price_label)
            layout.addLayout(hbox)

        layout.addWidget(self.total_label)

        # Блок с вводом даты рождения
        self.birth_date_label = QLabel("Выберите дату рождения:")
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate.currentDate())
        self.calc_age_button = QPushButton("Рассчитать возраст")
        self.calc_age_button.clicked.connect(self.calculate_age)
        self.age_info = QTextEdit()
        self.age_info.setReadOnly(True)

        layout.addWidget(self.birth_date_label)
        layout.addWidget(self.birth_date_input)
        layout.addWidget(self.calc_age_button)
        layout.addWidget(self.age_info)

        self.setLayout(layout)
        self.setWindowTitle("Программа PyQt6")
        self.show()

    def update_season_info(self):
        for season, btn in self.season_buttons.items():
            if btn.isChecked():
                self.season_label.setText(get_season_info(season))
                break

    def toggle_product(self, checkbox, quantity):
        quantity.setEnabled(checkbox.isChecked())
        font = QFont()
        font.setBold(checkbox.isChecked())
        checkbox.setFont(font)
        self.calculate_total()

    def calculate_total(self):
        total = 0
        for name, (checkbox, quantity, price, price_label) in self.product_widgets.items():
            if checkbox.isChecked():
                cost = quantity.value() * price
                total += cost
                price_label.setText(f"Цена: {price} руб. | Итог: {cost:.2f} руб.")
            else:
                price_label.setText(f"Цена: {price} руб.")
        self.total_label.setText(f"Общая стоимость: {total:.2f} руб.")

    def calculate_age(self):
        birth_date = self.birth_date_input.date().toPyDate()
        today = QDate.currentDate().toPyDate()
        age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        age_days = (today - birth_date).days
        age_hours = age_days * 24
        age_seconds = age_hours * 3600

        self.age_info.setHtml(f"""
            <b>Ваш возраст:</b><br>
            <ul>
                <li><b>Лет:</b> {age_years}</li>
                <li><b>Часов:</b> {age_hours:,}</li>
                <li><b>Секунд:</b> {age_seconds:,}</li>
            </ul>
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
