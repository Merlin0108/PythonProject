from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class TextView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.labels = {}

        # Статические подписи
        self.freq_label = QLabel()
        self.min_label = QLabel()
        self.max_label = QLabel()
        self.mean_label = QLabel()
        self.mode_label = QLabel()

        self.layout.addWidget(self.freq_label)
        self.layout.addWidget(self.min_label)
        self.layout.addWidget(self.max_label)
        self.layout.addWidget(self.mean_label)
        self.layout.addWidget(self.mode_label)

    def update_text(self, frequencies, minimum, maximum, mean, mode):
        if not frequencies:
            self.freq_label.setText("Данные отсутствуют")
            self.min_label.setText("")
            self.max_label.setText("")
            self.mean_label.setText("")
            self.mode_label.setText("")
            return

        freq_text = "Частоты:\n"
        for num, count in sorted(frequencies.items()):
            freq_text += f"  {num}: {count} раз(а)\n"

        self.freq_label.setText(freq_text)
        self.min_label.setText(f"Минимум: {minimum}")
        self.max_label.setText(f"Максимум: {maximum}")
        self.mean_label.setText(f"Среднее: {mean:.2f}")
        self.mode_label.setText(f"Мода: {mode if mode is not None else 'нет'}")
