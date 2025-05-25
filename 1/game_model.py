import json
from PyQt5.QtCore import QObject, pyqtSignal


class GameModel(QObject):
    stateChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.total_stones = 20
        self.remaining_stones = 20
        self.current_player = 1
        self.game_mode = "PvsAI"
        self.win_condition = "Взять последний"
        self.is_game_over = False

    def new_game(self, stones, game_mode, win_condition):
        if not (5 <= stones <= 100):
            raise ValueError("Количество камней должно быть от 5 до 100.")
        self.total_stones = stones
        self.remaining_stones = stones
        self.current_player = 1
        self.game_mode = game_mode
        self.win_condition = win_condition
        self.is_game_over = False
        self.stateChanged.emit()

    def make_move(self, taken):
        if self.is_game_over or taken < 1 or taken > 4 or taken > self.remaining_stones:
            return False
        self.remaining_stones -= taken
        if self.remaining_stones == 0:
            self.is_game_over = True
        else:
            self.current_player = 2 if self.current_player == 1 else 1
        self.stateChanged.emit()
        return True

    def get_winner(self):
        if not self.is_game_over:
            return None
        return self.current_player if self.win_condition == "Взять последний" else 2 if self.current_player == 1 else 1

    def ai_move(self):
        for take in range(1, 5):
            remaining = self.remaining_stones - take
            if self.win_condition == "Взять последний" and remaining % 5 == 0:
                return take
            if self.win_condition == "Оставить последний" and remaining % 5 == 1:
                return take
        return min(4, self.remaining_stones)

    def save_state(self, path):
        with open(path, "w") as f:
            json.dump({
                "total": self.total_stones,
                "remaining": self.remaining_stones,
                "player": self.current_player,
                "mode": self.game_mode,
                "win": self.win_condition
            }, f)

    def load_state(self, path):
        with open(path) as f:
            data = json.load(f)
        self.new_game(int(data["total"]), data["mode"], data["win"])
        self.remaining_stones = int(data["remaining"])
        self.current_player = int(data["player"])
        self.is_game_over = (self.remaining_stones == 0)
        self.stateChanged.emit()
