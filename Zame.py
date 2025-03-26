from PyQt5.QtCore import (Qt, QAbstractListModel, QModelIndex, QDateTime)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QListView, QAction, QMenu, QDialog, QLineEdit,
                             QDateTimeEdit, QDialogButtonBox, QLabel)

class Note:
    def __init__(self, text, date):
        self.text = text
        self.date = date

class NoteModel(QAbstractListModel):
    def __init__(self, notes=None):
        super().__init__()
        self.notes = notes or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.notes)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        note = self.notes[index.row()]
        return f"{note.date.toString('yyyy-MM-dd HH:mm')}: {note.text}"

    def addNote(self, text, date):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.notes.append(Note(text, date))
        self.endInsertRows()

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole and index.isValid():
            text, date = value
            self.notes[index.row()].text = text
            self.notes[index.row()].date = date
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsEditable | super().flags(index)

class NoteDialog(QDialog):
    def __init__(self, parent=None, text="", date=None):
        super().__init__(parent)
        self.setWindowTitle("Заметка")
        layout = QVBoxLayout()
        self.text_edit = QLineEdit(text)
        self.date_edit = QDateTimeEdit(date if date else QDateTime.currentDateTime())
        layout.addWidget(QLabel("Текст:"))
        layout.addWidget(self.text_edit)
        layout.addWidget(QLabel("Дата:"))
        layout.addWidget(self.date_edit)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_data(self):
        return (self.text_edit.text(), self.date_edit.dateTime())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = NoteModel()
        self.setup_ui()
        self.setup_menus()

    def setup_ui(self):
        self.setWindowTitle("Заметки")
        central_widget = QWidget()
        layout = QVBoxLayout()
        self.list_view = QListView()
        self.list_view.setModel(self.model)
        layout.addWidget(self.list_view)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.list_view.doubleClicked.connect(self.edit_note)

    def setup_menus(self):
        menu_bar = self.menuBar()
        edit_menu = menu_bar.addMenu("Правка")
        add_action = QAction("Добавить", self)
        add_action.triggered.connect(self.add_note)
        edit_action = QAction("Изменить", self)
        edit_action.triggered.connect(self.edit_note)
        edit_menu.addAction(add_action)
        edit_menu.addAction(edit_action)
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu()
        add_action = QAction("Добавить", self)
        add_action.triggered.connect(self.add_note)
        edit_action = QAction("Изменить", self)
        edit_action.triggered.connect(self.edit_note)
        menu.addAction(add_action)
        menu.addAction(edit_action)
        menu.exec_(self.list_view.viewport().mapToGlobal(pos))

    def add_note(self):
        dialog = NoteDialog(self)
        if dialog.exec() == QDialog.Accepted:
            text, date = dialog.get_data()
            self.model.addNote(text, date)

    def edit_note(self):
        index = self.list_view.currentIndex()
        if index.isValid():
            note = self.model.notes[index.row()]
            dialog = NoteDialog(self, note.text, note.date)
            if dialog.exec() == QDialog.Accepted:
                new_text, new_date = dialog.get_data()
                self.model.setData(index, (new_text, new_date))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()