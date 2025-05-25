import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from start_dialog import StartDialog
from game_model import GameModel


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Показываем стартовый диалог
    start_dialog = StartDialog()
    if start_dialog.exec_() == start_dialog.Accepted:
        result = start_dialog.result
        model = GameModel()
        if result[0] == 'new':
            stones, mode, win = result[1]
            model.new_game(stones, mode, win)
        elif result[0] == 'load':
            model.load_state(result[1])
        else:
            sys.exit()

        window = MainWindow()
        window.model = model
        window.model.stateChanged.connect(window.update_view)
        window.update_view()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()
