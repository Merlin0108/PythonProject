from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtCore import Qt

class ChartView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frequencies = {}

    def set_frequencies(self, freq_dict):
        self.frequencies = freq_dict
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()
        margin = 40

        if not self.frequencies:
            painter.drawText(width//2 - 50, height//2, "Нет данных")
            return

        keys = sorted(self.frequencies.keys())
        values = [self.frequencies[k] for k in keys]

        max_value = max(values)
        bar_width = (width - 2*margin) / len(keys)

        font = QFont("Arial", 9)
        painter.setFont(font)



        # Рисуем бары
        for i, key in enumerate(keys):
            val = self.frequencies[key]
            bar_height = (val / max_value) * (height - 2*margin)

            x = margin + i * bar_width
            y = height - margin - bar_height

            # Заливка
            painter.setBrush(QColor(100, 150, 255))
            painter.setPen(QPen(Qt.black))
            painter.drawRect(int(x), int(y), int(bar_width*0.8), int(bar_height))

            # Подписи под столбцами
            painter.drawText(int(x), height - margin + 15, str(key))

            # Подписи над столбцами
            painter.drawText(int(x), int(y) - 5, str(val))
