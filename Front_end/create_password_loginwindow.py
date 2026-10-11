from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from qfluentwidgets import PasswordLineEdit, PushButton, setTheme, Theme, setCustomStyleSheet, IconWidget, \
    FluentIcon as FIF
from password_verification import password_authentecation
from verification.verification import create_vault_user

class LoginWindow(QWidget):
    # ვქმნით სიგნალს, რომელიც გადასცემს True-ს წარმატების შემთხვევაში
    success_signal = pyqtSignal(bytes)
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)

        self.showMaximized()
        self.setWindowTitle('Vault Guard')
        self.setWindowIcon(QIcon('vaulticon.webp'))


        self.main_layout = QVBoxLayout(self)

        self.login_card = QFrame()

        self.title = QLabel('Create Master Password')
        self.password_label = QLabel('Password:')
        self.confirm_password_label = QLabel('Confirm Password:')

        self.password = PasswordLineEdit()
        self.confirm_password = PasswordLineEdit()

        self.create_password = PushButton('Create', self)
        self.title_card = QLabel('Vault Guard', self)

        self.shield_icon = QLabel(self)

        self.requirements = QLabel(self)

        self.show_create_master_password()

    def show_create_master_password(self):
        # 1. Base Stylesheet - Targets specific component types cleanly with overrides
        self.setStyleSheet("""
            LoginWindow {
                background-color: rgb(65, 65, 66); 
            }
        """)

        setCustomStyleSheet(
            self.create_password,
            '',
            """
                PushButton {
                    background-color: rgb(0, 120, 215);
                    border: 1px solid rgb(0, 90, 158);
                    border-radius: 8px;
                    color: black;
                    font-size: 25px;
                    font-weight: bold;
                }
                PushButton:hover { background-color: rgb(24, 141, 242); }
                PushButton:pressed { background-color: rgb(0, 90, 158); }
            """
        )
        self.password.setStyleSheet("background-color: rgb(207, 207, 207);")
        self.confirm_password.setStyleSheet("background-color: rgb(207, 207, 207);")

        # 2. Outer Layout Setup (Keeps everything visually balanced)
        self.main_layout.addStretch(1)

        title_row = QHBoxLayout()
        title_row.addStretch()
        title_row.addWidget(self.shield_icon)
        title_row.addSpacing(10)
        title_row.addWidget(self.title_card)
        title_row.addStretch()

        self.main_layout.addLayout(title_row)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.login_card, alignment=Qt.AlignCenter)
        self.main_layout.addStretch(1)

        # 3. Handle Header Configuration
        self.title_card.setFixedSize(350, 80)
        self.title_card.setAlignment(Qt.AlignCenter)
        self.title_card.setStyleSheet("""
            font-family: 'Segoe UI Variable Display', 'Segoe UI', Arial;
            font-size: 60px;
            font-weight: bold;
            color: white;
            background-color: transparent;
        """)

        # 4. Handle Login Card Container
        self.login_card.setFixedSize(600, 480)
        self.login_card.setStyleSheet("""
            QFrame {
                background-color: rgb(92, 184, 255);
                border: 1px solid #2d2d2d;
                border-radius: 12px;
            }
        """)

        # 5. Font Sizing for Password Fields
        input_font = QFont("Segoe UI", 16)
        self.password.setFont(input_font)
        self.confirm_password.setFont(input_font)

        # 6. Configure Input Field Labels
        label_style = """
            color: black;
            font-weight: bold;
            font-size: 20px;
            font-family: 'Segoe UI', Arial;
            border-radius: 4px;
            padding-left: 5px;
        """
        self.password_label.setFixedWidth(180)
        self.password_label.setStyleSheet(label_style)

        self.confirm_password_label.setFixedWidth(180)
        self.confirm_password_label.setStyleSheet(label_style)

        # 7. Layout inside the login card panel
        inner_vertical = QVBoxLayout(self.login_card)
        inner_vertical.setContentsMargins(40, 40, 40, 40)

        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: black;
            background-color: transparent;
        """)
        self.title.setFixedHeight(50)

        # 8. Assemble Field Rows
        inner_horizontal1 = QHBoxLayout()
        inner_horizontal2 = QHBoxLayout()
        inner_horizontal3 = QHBoxLayout()
        inner_horizontal4 = QHBoxLayout()

        inner_horizontal1.addWidget(self.password_label)
        inner_horizontal1.addWidget(self.password)

        inner_horizontal2.addWidget(self.confirm_password_label)
        inner_horizontal2.addWidget(self.confirm_password)

        # 9 icon
        icon_pixmap = FIF.FINGERPRINT.icon().pixmap(50, 50)
        self.shield_icon.setPixmap(icon_pixmap)
        self.shield_icon.setFixedSize(50, 50)
        self.shield_icon.setStyleSheet("background-color: transparent;")

        # ღილაკის ცენტრში დაყენება
        inner_horizontal3.addStretch()
        self.create_password.setFixedSize(180, 45)
        inner_horizontal3.addWidget(self.create_password)
        inner_horizontal3.addStretch()

        # პაროლის საჭიროების label
        self.requirements.setStyleSheet('font-size: 16px;'
                                        'font-style: Arial;'
                                        'color: rgb(135, 0, 7)')
        self.requirements.setVisible(False)
        inner_horizontal4.addWidget(self.requirements)

        # Build Card Structure
        inner_vertical.addWidget(self.title)
        inner_vertical.addSpacing(30)
        inner_vertical.addLayout(inner_horizontal1)
        inner_vertical.addSpacing(25)
        inner_vertical.addLayout(inner_horizontal2)
        inner_vertical.addSpacing(35)
        inner_vertical.addLayout(inner_horizontal3)
        inner_vertical.addSpacing(25)
        inner_vertical.addLayout(inner_horizontal4)
        inner_vertical.addStretch()

        # 9. Clean Elevation Dropshadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setYOffset(12)
        shadow.setXOffset(0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.login_card.setGraphicsEffect(shadow)

        # 10 პაროლის შემოწმების lineedit-ი აქტიური იყოს მხოლოდ მაშინ, როცა პაროლს შეიყვან
        self.confirm_password.setEnabled(False)
        #  connections
        self.password.textChanged.connect(self.password_typed)
        self.create_password.clicked.connect(self.password_requirements)

    def password_typed(self, text):
        if text:
            self.confirm_password.setEnabled(True)
        else:
            self.confirm_password.setEnabled(False)
            self.confirm_password.clear()

        # 11 ღილაკის დაჭერის შემდეგ პაროლის შემოწმება

    def password_requirements(self):
        password = self.confirm_password.text()

        if not password_authentecation(password):
            self.requirements.setVisible(True)
            self.requirements.setText(
                'Requires at least 8 charachters\nAnd at least one upper letter, lower letter, digit and special symbol')
            return
        if password != self.confirm_password.text():
            self.requirements.setText('The passwords must be same')
            self.requirements.setVisible(True)
            return

        self.requirements.setVisible(False)
        key = create_vault_user(password)
        self.success_signal.emit(key)




