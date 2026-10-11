from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from qfluentwidgets import PasswordLineEdit, PushButton, setTheme, Theme, setCustomStyleSheet, IconWidget, FluentIcon as FIF
from verification.verification import verify_vault_user, VaultNotFoundError, WrongPasswordError

class LoginWindow(QWidget):
    # ვქმნით სიგნალს, რომელიც გადასცემს True-ს წარმატების შემთხვევაში
    success_signal = pyqtSignal(bytes)
    def __init__(self):
        super().__init__()
        # მუქი ფერისტვის
        setTheme(Theme.DARK)
        # ფანჯარას შეეძლება მტლიან ეკრანზე გაფართოება და არ არის საჭირო ზომის ხელით შერჩევა
        self.showMaximized()
        # ფანჯრის სათაური და icon-ის დამატება
        self.setWindowTitle('Vault Guard')
        self.setWindowIcon(QIcon('vaulticon.webp'))
        # მთავარი layout სატაურისა და login card-ის დასაწყობად
        self.main_layout = QVBoxLayout(self)
        # გამოყენებულია QFrame ფორმის შესააქმნელად
        self.login_card = QFrame()

        self.title = QLabel('Enter Master Password')
        self.password_label = QLabel('Password:')

        self.password = PasswordLineEdit()

        self.enter_password = PushButton('Enter', self)
        self.title_card = QLabel('Vault Guard', self)

        self.shield_icon = QLabel(self)

        self.requirements = QLabel(self)

        self.show_create_master_password()

    def show_create_master_password(self):
        # 1. უკანა ფონტი დავადე stylesheet-ის დახმარებით
        self.setStyleSheet("""
            LoginWindow {
                background-color: rgb(65, 65, 66); 
            }
        """)
        # აქ შესასვლელ ღილაკზე გამოვიყენე Stylesheet ვიზუალისთვის hover ღილაკზე გადასვლისას ფერი ეცვლება
        setCustomStyleSheet(
            self.enter_password,
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
        # რადგან პაროლის Line edit-ი ფერს უკანაფონთან მიმართებაში იცვლის საჭიროა საკუთარი ფერის დამატება
        self.password.setStyleSheet("background-color: rgb(207, 207, 207);")

        # 2. Outer Layout Setup (Keeps everything visually balanced)
        self.main_layout.addStretch(1)

        title_row = QHBoxLayout()
        title_row.addStretch()
        title_row.addWidget(self.shield_icon)
        title_row.addSpacing(10)
        title_row.addWidget(self.title_card)
        title_row.addStretch()

        self.main_layout.addLayout(title_row)
        self.main_layout.addSpacing(30)
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

        inner_horizontal1.addWidget(self.password_label)
        inner_horizontal1.addWidget(self.password)

        # 9 icon
        icon_pixmap = FIF.FINGERPRINT.icon().pixmap(50, 50)
        self.shield_icon.setPixmap(icon_pixmap)
        self.shield_icon.setFixedSize(50, 50)
        self.shield_icon.setStyleSheet("background-color: transparent;")

        # ღილაკის ცენტრში დაყენება
        inner_horizontal2.addStretch()
        self.enter_password.setFixedSize(180, 45)
        inner_horizontal2.addWidget(self.enter_password)
        inner_horizontal2.addStretch()

        # პაროლის საჭიროების label
        self.requirements.setStyleSheet('font-size: 16px;'
                                        'font-style: Arial;'
                                        'color: rgb(135, 0, 7)')
        self.requirements.setVisible(False)
        inner_horizontal3.addWidget(self.requirements)

        # Build Card Structure
        inner_vertical.addWidget(self.title)
        inner_vertical.addSpacing(60)
        inner_vertical.addLayout(inner_horizontal1)
        inner_vertical.addSpacing(50)
        inner_vertical.addLayout(inner_horizontal3)
        inner_vertical.addSpacing(60)
        inner_vertical.addLayout(inner_horizontal2)
        inner_vertical.addStretch()

        # 9. Clean Elevation Dropshadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setYOffset(12)
        shadow.setXOffset(0)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.login_card.setGraphicsEffect(shadow)

        # 10 პაროლის შემოწმების lineedit-ი აქტიური იყოს მხოლოდ მაშინ, როცა პაროლს შეიყვან
        #  connections

        # 11 ღილაკის დაჭერის შემდეგ პაროლის შემოწმება
        #  connections
        self.enter_password.clicked.connect(self.password_requirements)
    def password_requirements(self):
        try:
            key = verify_vault_user(self.password.text())
        except WrongPasswordError:
            self.requirements.setVisible(True)
            self.requirements.setText('Incorrect Password')
            return
        except VaultNotFoundError:
            self.requirements.setVisible(True)
            self.requirements.setText('No vault found — please create one first')
            return

        if key is None:
            self.requirements.setVisible(True)
            self.requirements.setText('Incorrect Password')

        self.requirements.setVisible(False)
        self.success_signal.emit(key)

