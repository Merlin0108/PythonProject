import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWizard, QWizardPage,
    QVBoxLayout, QLineEdit, QListWidget, QCheckBox,
    QLabel, QPushButton, QTextEdit, QWidget
)
from PyQt5.QtCore import Qt, QTimer


class RegistrationWizard(QWizard):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация пользователя")
        self.addPage(LoginPage())
        self.addPage(InfoPage())
        self.addPage(InterestsPage())


class LoginPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Логин и пароль")
        layout = QVBoxLayout()

        self.login_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Логин:"))
        layout.addWidget(self.login_edit)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_edit)

        self.setLayout(layout)
        self.registerField('login*', self.login_edit)
        self.registerField('password*', self.password_edit)


class InfoPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("ФИО")
        layout = QVBoxLayout()

        self.name_edit = QLineEdit()
        layout.addWidget(QLabel("ФИО:"))
        layout.addWidget(self.name_edit)

        self.setLayout(layout)
        self.registerField('name*', self.name_edit)


class InterestsPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Интересы")
        layout = QVBoxLayout()

        self.topics_list = QListWidget()
        self.topics_list.addItems(["Программирование", "Дизайн", "Маркетинг"])
        self.topics_list.setSelectionMode(QListWidget.MultiSelection)

        self.newsletter_check = QCheckBox("Согласен на рассылку")

        layout.addWidget(QLabel("Выберите интересы:"))
        layout.addWidget(self.topics_list)
        layout.addWidget(self.newsletter_check)

        self.setLayout(layout)
        self.registerField('newsletter', self.newsletter_check)

    def validatePage(self):
        selected = [item.text() for item in self.topics_list.selectedItems()]
        self.wizard().setProperty('topics', selected)
        return True


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Главное окно")
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.btn_start = QPushButton("Запустить мастер")
        self.btn_start.clicked.connect(self.run_wizard)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        layout.addWidget(self.btn_start)
        layout.addWidget(self.text_output)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def run_wizard(self):
        wizard = RegistrationWizard(self)
        if wizard.exec_() == QWizard.Accepted:
            # Получаем данные через QWizard.property()
            login = wizard.field("login")
            password = wizard.field("password")
            name = wizard.field("name")
            topics = wizard.property("topics") or []
            newsletter = "Да" if wizard.field("newsletter") else "Нет"

            output = (
                f"Логин: {login}\n"
                f"Пароль: {password}\n"
                f"ФИО: {name}\n"
                f"Интересы: {', '.join(topics)}\n"
                f"Рассылка: {newsletter}"
            )
            self.text_output.setPlainText(output)

        # Принудительно удаляем объект Wizard
        QTimer.singleShot(0, wizard.deleteLater)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())