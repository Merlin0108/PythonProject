import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from game_model import GameModel
from dialogs import NewGameDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Игра с кучкой камней")
        self.setFixedSize(600, 500)

        self.model = GameModel()
        self.model.stateChanged.connect(self.update_view)

        self.init_ui()
        self.update_view()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.info_label = QLabel("", self)
        self.info_label.setFont(QFont("Arial", 16))
        self.layout.addWidget(self.info_label, alignment=Qt.AlignCenter)

        self.display_info_label = QLabel("", self)
        self.display_info_label.setFont(QFont("Arial", 10))
        self.display_info_label.setStyleSheet("color: gray")
        self.layout.addWidget(self.display_info_label, alignment=Qt.AlignCenter)

        self.stone_layout = QHBoxLayout()
        self.layout.addLayout(self.stone_layout)

        self.selection_label = QLabel("Выберите камни для взятия (1-4): 0", self)
        self.layout.addWidget(self.selection_label, alignment=Qt.AlignCenter)

        self.take_button = QPushButton("Взять камни", self)
        self.take_button.clicked.connect(self.take_turn)
        self.layout.addWidget(self.take_button, alignment=Qt.AlignCenter)

        self.save_button = QPushButton("Сохранить игру")
        self.save_button.clicked.connect(self.save_game)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Загрузить игру")
        self.load_button.clicked.connect(self.load_game)
        self.layout.addWidget(self.load_button)

        self.new_button = QPushButton("Новая игра")
        self.new_button.clicked.connect(self.setup_new_game)
        self.layout.addWidget(self.new_button)

        self.selected_count = 0
        self.selected_indices = set()
        self.stone_labels = []

    def setup_new_game(self):
        dialog = NewGameDialog(self)
        if dialog.exec_():
            stones, mode, win = dialog.get_settings()
            try:
                self.model.new_game(stones, mode, win)
            except ValueError as e:
                self.show_message(str(e))

    def update_view(self):
        self.clear_stones()
        total = self.model.remaining_stones
        self.display_info_label.setText(
            f"Всего камней: {total}. Отображаются последние 10." if total > 10 else ""
        )
        self.info_label.setText(f"Ход игрока {self.model.current_player}")
        self.selection_label.setText(f"Выберите камни для взятия (1-4): {self.selected_count}")
        self.take_button.setEnabled(self.model.current_player == 1 or self.model.game_mode == "PvsP")

        show_count = min(10, total)
        display_offset = total - show_count

        for i in range(show_count):
            lbl = QLabel("💎", self)
            lbl.setFont(QFont("Arial", 32))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("color: darkblue; background-color: none")
            idx = display_offset + i
            lbl.mousePressEvent = lambda e, real_idx=idx, lbl_ref=lbl: self.select_stone(real_idx, lbl_ref)
            self.stone_layout.addWidget(lbl)
            self.stone_labels.append(lbl)

        if self.model.is_game_over:
            winner = self.model.get_winner()
            self.show_message(f"Игрок {winner} победил!")
            self.take_button.setEnabled(False)

        if self.model.current_player == 2 and self.model.game_mode == "PvsAI" and not self.model.is_game_over:
            self.take_button.setEnabled(False)
            QTimer.singleShot(1000, self.ai_turn)

    def clear_stones(self):
        for lbl in self.stone_labels:
            self.stone_layout.removeWidget(lbl)
            lbl.deleteLater()
        self.stone_labels.clear()
        self.selected_indices.clear()
        self.selected_count = 0
        self.display_info_label.clear()

    def select_stone(self, index, label):
        if self.model.current_player == 2 and self.model.game_mode == "PvsAI":
            return
        if index in self.selected_indices:
            self.selected_indices.remove(index)
            self.selected_count -= 1
            label.setStyleSheet("color: darkblue; background-color: none")
        elif self.selected_count < 4:
            self.selected_indices.add(index)
            self.selected_count += 1
            label.setStyleSheet("color: darkblue; background-color: yellow")
        self.selection_label.setText(f"Выберите камни для взятия (1-4): {self.selected_count}")

    def take_turn(self):
        if not 1 <= self.selected_count <= 4:
            self.show_message("Выберите от 1 до 4 камней.")
            return
        if self.selected_count > self.model.remaining_stones:
            self.show_message("Слишком много камней выбрано.")
            return
        ok = self.model.make_move(self.selected_count)
        if not ok:
            self.show_message("Некорректный ход.")
        else:
            self.selected_count = 0
            self.selection_label.setText("Выберите камни для взятия (1-4): 0")

    def ai_turn(self):
        if self.model.current_player != 2 or self.model.is_game_over:
            return
        take = self.model.ai_move()
        self.model.make_move(take)

    def save_game(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить игру", "", "JSON Files (*.json)")
        if path:
            self.model.save_state(path)

    def load_game(self):
        path, _ = QFileDialog.getOpenFileName(self, "Загрузить игру", "", "JSON Files (*.json)")
        if path:
            self.model.load_state(path)

    def show_message(self, text):
        QMessageBox.information(self, "Сообщение", text)
