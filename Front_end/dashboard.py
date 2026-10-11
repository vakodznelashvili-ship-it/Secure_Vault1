from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from qfluentwidgets import (CardWidget, SubtitleLabel)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame, QListWidget)


class DashBoardPage(QWidget):
    def __init__(self):
        super().__init__()
        # ობიექტის სახელი
        self.setObjectName('DashboardPage')
        # ფანჯრის სახელი
        self.setWindowTitle("Dashboard")
        # ვიჯეტების სამართავად შევქმენი მთავარი ლეიაუთი
        self.main_dashboard_layout = QVBoxLayout(self)
        # სათაური
        self.title = QLabel(self)

        # პაროლების შესახებ ინფორმაციის გამოსაჩენად შევქმენი ეს ვიჯეტი
        self.passwordframe = QFrame()
        # პაროლოის ვიჯეტის შიგნით ინფორმაციის გამოსაჩენად და დასალაგებლად კიდევ შევქმენი შიდა ლეიაუთი
        self.passwordframe_layout = QVBoxLayout(self.passwordframe)
        # სათაური
        self.passwordframe_title = QLabel()
        # პაროლების გამოსაჩენი ტექსტი
        self.password_count = QLabel()
        # პაროლების მთლიანი რიცხვის გამოჩენა ეს ცალკეა რათა უფრო მართივი იყოს რიცხვის გამოჩენა
        self.password_sum = QLabel()
        # საფრთხის შემცველი პაროლების რაოდენობა ტექსტი და რივიც ერთად
        self.unsafe_passwords = QLabel()
        # ძლიერი პაროლების რაოდენობა ტექსტი და რივიც ერთად
        self.strong_passwords = QLabel()

        # ფაილების შესახებ ინფორმაციის გამოსაჩენად შევქმენი ეს ვიჯეტი
        self.fileframe = QFrame()
        # ფაილის ვიჯეტის შიგნით ინფორმაციის გამოსაჩენად და დასალაგებლად კიდევ შევქმენი შიდა ლეიაუთი
        self.fileframe_layout = QVBoxLayout(self.fileframe)
        # სათაური
        self.fileframe_title = QLabel()
        # ფაილების გამოსაჩენი ტექსტი
        self.file_count = QLabel()
        # ფაილების მთლიანი რიცხვის გამოჩენა ეს ცალკეა რათა უფრო მართივი იყოს რიცხვის გამოჩენა
        self.file_sum = QLabel()
        # საფრთხის შემცველი ფაილების რაოდენობა ტექსტი და რიცხვიც ერთად
        self.unsafe_file = QLabel()
        # კარანტინში არსებული ფაილების რაოდენობა ტექსტი და რიცხვიც ერთად
        self.quarantine_file = QLabel()

        # საფრთხის შესახებ ინფორმაციის გამოსაჩენად შევქმენი ეს ვიჯეტი
        self.threatframe = QFrame()
        # საფრთხის ვიჯეტის შიგნით ინფორმაციის გამოსაჩენად და დასალაგებლად კიდევ შევქმენი შიდა ლეიაუთი
        self.threatframe_layout = QVBoxLayout(self.threatframe)
        # სათაური
        self.threatframe_title = QLabel()
        # საფრთხეების გამოსაჩენი ტექსტი
        self.threat_count = QLabel()
        # საფრთხეების მთლიანი რაოდენობის რიცხვითი მაჩვენებელი
        self.threat_sum = QLabel()
        # სუსტი პაროლებისგან გამოწვეული საფრთხეების რაოდენობა
        self.weak_passwords = QLabel()
        # არასაიმედო/საშიში ფაილების რაოდენობა
        self.unsafe_files = QLabel()

        # დუბლიკატი მონაცემების გამოსაჩენი ვიჯეტი
        self.duplicateframe = QFrame()
        # დუბლიკატების ვიჯეტის შიდა ლეიაუთი ელემენტების ვერტიკალურად დასალაგებლად
        self.duplicateframe_layout = QVBoxLayout(self.duplicateframe)
        # სათაური
        self.duplicateframe_title = QLabel()
        # დუბლიკატების გამოსაჩენი ტექსტი
        self.duplicate_count = QLabel()
        # დუბლიკატების მთლიანი რაოდენობის რიცხვითი მაჩვენებელი
        self.duplicate_sum = QLabel()
        # მეორებადი/დუბლირებული პაროლების რაოდენობა
        self.duplicate_of_passwords = QLabel()
        # მეორებადი/დუბლირებული ფაილების რაოდენობა
        self.duplicate_of_files = QLabel()

        # აქტიური შეტყობინებების (Alerts) კონტეინერი ბარათის სტილში
        self.alertsframe_message = CardWidget()
        # შეტყობინებების სიის ვიჯეტი, სადაც სათითაოდ დაემატება ქმედებები
        self.alerts_list = QListWidget()

        # ბლოკირებული საფრთხეების კონტეინერი ბარათის სტილში
        self.threatframe_message = CardWidget()
        # დაბლოკილი საფრთხეების სიის ვიჯეტი
        self.threats_list = QListWidget()

        # ინტერფეისის ვიზუალური მხარის ამწყობი მეთოდის გამოძახება
        self.Ui()

    def Ui(self):
        # სტილისტური ცვლილებები ფანჯარაზე (დაშორებები ელემენტებს შორის და ჩარჩოდან)
        self.main_dashboard_layout.setSpacing(40)
        self.main_dashboard_layout.setContentsMargins(30, 30, 30, 30)

        # მთავარი გვერდის სათაურის ტექსტის დაყენება და ზომის განსაზღვრა
        self.title.setText("Dashboard Page")
        self.title.setFixedHeight(100)
        self.title.setStyleSheet('''
        font-size: 60px;
        font-weight: bold;
        font-family: Verdana;
        padding: 5px;
        color: white;
        ''')

        # შეტყობინებების და საფრთხეების პანელების საერთო დიზაინის CSS სტილი
        message_panel_style = """
                    background-color: rgb(153, 153, 153); 
                    border: 1px solid #2d2d2d; 
                    border-radius: 12px;
                """

        # სიის ელემენტების CSS სტილი — ზომის გაზრდა (22px) და ტექსტის გათეთრება
        self.alerts_list.setStyleSheet("""
            QListWidget { 
                background: transparent; 
                border: none; 
                padding: 5px;
            }
            QListWidget::item { 
                color: #ffffff;        /* თეთრი ტექსტი */
                font-size: 22px;       /* გაზრდილი ზომა */
                font-weight: bold;     /* გამუქებული */
                padding-bottom: 8px;   /* დაშორება შეტყობინებებს შორის */
            }
        """)

        # საფრთხეების სიის ელემენტების CSS სტილი — წითელი ფერი და 22px ზომა
        self.threats_list.setStyleSheet("""
            QListWidget { 
                background: transparent; 
                border: none; 
                padding: 5px;
            }
            QListWidget::item { 
                color: #ff4d4d;        /* მკვეთრი წითელი ტექსტი საფრთხეებისთვის */
                font-size: 22px;       /* გაზრდილი ზომა */
                font-weight: bold;     /* გამუქებული */
                padding-bottom: 8px;   
            }
        """)

        # საინფორმაციო ბარათების (Frames) ფონების ფერებისა და კუთხეების მომრგვალების დაყენება
        self.passwordframe.setStyleSheet('Background: rgb(28, 255, 32); border-radius: 40px;')
        self.fileframe.setStyleSheet('Background: rgb(255, 28, 51); border-radius: 40px;')
        self.duplicateframe.setStyleSheet('Background: rgb(79, 120, 255); border-radius: 40px;')
        self.threatframe.setStyleSheet('Background: rgb(250, 184, 52); border-radius: 40px;')

        # შეტყობინებების პანელებზე ზემოთ შექმნილი სტილის მინიჭება
        self.alertsframe_message.setStyleSheet(message_panel_style)
        self.threatframe_message.setStyleSheet(message_panel_style)

        # საინფორმაციო ბარათების და ქვედა დიდი პანელების მინიმალური ზომების განსაზღვრა
        self.passwordframe.setMinimumSize(200, 150)
        self.fileframe.setMinimumSize(200, 150)
        self.threatframe.setMinimumSize(200, 150)
        self.duplicateframe.setMinimumSize(200, 150)
        self.alertsframe_message.setMinimumSize(400, 350)
        self.threatframe_message.setMinimumSize(400, 350)

        # ბადისებრი (Grid) ლეიაუთის შექმნა 4 მთავარი საინფორმაციო ბარათისთვის
        cards1 = QGridLayout()
        cards1.setSpacing(15)
        cards1.setContentsMargins(10, 10, 10, 10)

        # ბარათების განთავსება პირველ რიგში (ინდექსი 0), სხვადასხვა სვეტებში (0-დან 3-მდე)
        cards1.addWidget(self.passwordframe, 0, 0)
        cards1.addWidget(self.fileframe, 0, 1)
        cards1.addWidget(self.threatframe, 0, 2)
        cards1.addWidget(self.duplicateframe, 0, 3)

        # მეორე ბადისებრი ლეიაუთის შექმნა ქვედა შეტყობინებების პანელებისთვის
        cards2 = QGridLayout()
        cards2.setSpacing(15)
        cards2.setContentsMargins(10, 10, 10, 10)

        # შეტყობინებებისა და საფრთხეების დიდი ბარათების გვერდიგვერდ განთავსება
        cards2.addWidget(self.alertsframe_message, 0, 0)
        cards2.addWidget(self.threatframe_message, 0, 1)

        # სვეტების პროპორციულად გაწელვა, რომ თანაბარი ადგილი დაიკავონ
        cards2.setColumnStretch(0, 1)
        cards2.setColumnStretch(1, 1)

        # მთავარ ლეიაუთში სათაურის და ორივე ბლოკის (ბარათების და შეტყობინებების) დამატება
        self.main_dashboard_layout.addWidget(self.title)
        self.main_dashboard_layout.addLayout(cards1)
        self.main_dashboard_layout.addLayout(cards2)

        # --- პაროლების ბარათის შიდა ელემენტების ტექსტები და სტილები ---
        self.passwordframe_title.setText("🔒 Passwords")
        self.passwordframe_title.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.passwordframe_layout.addWidget(self.passwordframe_title)

        self.password_count.setText("Total number of passwords")
        self.password_count.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.passwordframe_layout.addWidget(self.password_count)

        self.password_sum.setText(f"0")
        self.password_sum.setStyleSheet("font-size: 80px; font-weight: bold; color: black;")
        self.passwordframe_layout.addWidget(self.password_sum, alignment=Qt.AlignCenter)

        self.unsafe_passwords.setText(f"❌ Weak passwords: 0")
        self.unsafe_passwords.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.passwordframe_layout.addWidget(self.unsafe_passwords)

        self.strong_passwords.setText(f"✅ Strong passwords: 0")
        self.strong_passwords.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.passwordframe_layout.addWidget(self.strong_passwords)

        # --- ფაილების ბარათის შიდა ელემენტების ტექსტები და სტილები ---
        self.fileframe_title.setText("📁 Files")
        self.fileframe_title.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.fileframe_layout.addWidget(self.fileframe_title)

        self.file_count.setText("Total number of files")
        self.file_count.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.fileframe_layout.addWidget(self.file_count)

        self.file_sum.setText(f"0")
        self.file_sum.setStyleSheet("font-size: 80px; font-weight: bold; color: black;")
        self.fileframe_layout.addWidget(self.file_sum, alignment=Qt.AlignCenter)

        self.unsafe_file.setText(f"✖️ Unsafe files: 0")
        self.unsafe_file.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.fileframe_layout.addWidget(self.unsafe_file)

        self.quarantine_file.setText(f" 🔏 quarantined files: 0")
        self.quarantine_file.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.fileframe_layout.addWidget(self.quarantine_file)

        # --- საფრთხეების ბარათის შიდა ელემენტების ტექსტები და სტილები ---
        self.threatframe_title.setText("💣 Threats")
        self.threatframe_title.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.threatframe_layout.addWidget(self.threatframe_title)

        self.threat_count.setText("Total number of threats")
        self.threat_count.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.threatframe_layout.addWidget(self.threat_count)

        self.threat_sum.setText(f"0")
        self.threat_sum.setStyleSheet("font-size: 80px; font-weight: bold; color: black;")
        self.threatframe_layout.addWidget(self.threat_sum, alignment=Qt.AlignCenter)

        self.weak_passwords.setText(f"❌ Unsafe passwords: 0")
        self.weak_passwords.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.threatframe_layout.addWidget(self.weak_passwords)

        self.unsafe_files.setText(f"🗃️ Unsafe files: 0")
        self.unsafe_files.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.threatframe_layout.addWidget(self.unsafe_files)

        # --- დუბლიკატების ბარათის შიდა ელემენტების ტექსტები და სტილები ---
        self.duplicateframe_title.setText("🔎 Duplicate")
        self.duplicateframe_title.setStyleSheet("font-size: 30px; font-weight: bold; color: black;")
        self.duplicateframe_layout.addWidget(self.duplicateframe_title)

        self.duplicate_count.setText("Total number of duplicates")
        self.duplicate_count.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.duplicateframe_layout.addWidget(self.duplicate_count)

        self.duplicate_sum.setText(f"0")
        self.duplicate_sum.setStyleSheet("font-size: 80px; font-weight: bold; color: black;")
        self.duplicateframe_layout.addWidget(self.duplicate_sum, alignment=Qt.AlignCenter)

        self.duplicate_of_passwords.setText(f"🔑 Duplicate passwords: 0")
        self.duplicate_of_passwords.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.duplicateframe_layout.addWidget(self.duplicate_of_passwords)

        self.duplicate_of_files.setText(f"📁 Unsafe files: 0")
        self.duplicate_of_files.setStyleSheet("font-size: 22px; font-weight: bold; color: black;")
        self.duplicateframe_layout.addWidget(self.duplicate_of_files)

        # --- აქტიური შეტყობინებების (Alerts) კონტეინერის აწყობა ---
        alerts_layout = QVBoxLayout(self.alertsframe_message)
        alerts_layout.setContentsMargins(20, 20, 20, 20)
        alerts_layout.setSpacing(20)

        alerts_header = SubtitleLabel("⚠️ Active Alerts", self.alertsframe_message)
        alerts_header.setStyleSheet('color: black;')
        alerts_header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        alerts_layout.addWidget(alerts_header, alignment=Qt.AlignTop)

        # სიის ვიჯეტის მიბმა ლეიაუტთან
        alerts_layout.addWidget(self.alerts_list)

        # --- დაბლოკილი საფრთხეების (Threats) კონტეინერის აწყობა ---
        threat_layout = QVBoxLayout(self.threatframe_message)
        threat_layout.setContentsMargins(20, 20, 20, 20)
        threat_layout.setSpacing(20)

        threats_header = SubtitleLabel("🛑 Blocked Threats", self.threatframe_message)
        threats_header.setStyleSheet('color: black;')
        threats_header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        threat_layout.addWidget(threats_header, alignment=Qt.AlignTop)

        # საფრთხეების სიის ვიჯეტის მიბმა ლეიაუტთან
        threat_layout.addWidget(self.threats_list)

    def event_log(self, event_code: int, details: str = ""):
        """სისტემური მოვლენების ჟურნალი კოდების მიხედვით"""
        match event_code:
            # 100 კოდი აღწერს პაროლებთან დაკავშირებულ მოვლენებს
            case 101:
                msg = f"🔑 [PASSWORD] New password created: ({details})"
                self.alerts_list.addItem(msg)
            case 102:
                msg = f"🔑 [PASSWORD] password edited: ({details})"
                self.alerts_list.addItem(msg)
            case 103:
                msg = f"🔑 [PASSWORD] Password deleted: ({details})"
                self.alerts_list.addItem(msg)
            case 104:
                msg = f"🔑 [PASSWORD] Similar password detected: ({details})"
                self.alerts_list.addItem(msg)
            case 105:
                msg = f"🔑 [PASSWORD] ({details}) password has not been updated for 90 days"
                self.alerts_list.addItem(msg)
            case 106:
                msg = f"🔑 [PASSWORD] ({details}) Clipboard contains copied password"
                self.alerts_list.addItem(msg)
            case 107:
                msg = f"🔑 [PASSWORD] ({details}) passwords imported"
                self.alerts_list.addItem(msg)
            # 200 კოდი აღწერს ფაილებთან დაკავშირებულ მოვლენებს
            case 201:
                msg = f"📁 [FILE] New file added: ({details})"
                self.alerts_list.addItem(msg)
            case 202:
                msg = f"📁 [FILE] File deleted: ({details})"
                self.alerts_list.addItem(msg)
            case 203:
                msg = f"📁 [FILE] ({details}) Duplicate file detected"
                self.alerts_list.addItem(msg)
            # 400 გამოიყენება საფრთხის აღმოცენის შემდეგ
            case 401:
                msg = f"⚠️ [RISK] Weak password vulnerability! ({details})"
                self.threats_list.addItem(msg)
            case 402:
                msg = f"⚠️ [RISK] Weak file vulnerability! ({details})"
                self.threats_list.addItem(msg)
            case 403:
                msg = f"⚠️ [RISK] Vault inactivity, closing ({details})"
                self.threats_list.addItem(msg)

    # --- კლასის გარე მეთოდები მონაცემთა ბაზასთან (SQL) დასაკავშირებლად ---

    def set_sum_passwords(self, num_passwords):
        """პაროლების მთლიანი რაოდენობის განახლება"""
        self.password_sum.setText(f"{num_passwords}")

    def unsafe_password_count(self, count):
        """სუსტი პაროლების მრიცხველის განახლება"""
        self.unsafe_passwords.setText(f"❌ Weak passwords: {count}")

    def strong_password_count(self, count):
        """ძლიერი პაროლების მრიცხველის განახლება"""
        self.strong_passwords.setText(f"✅ Strong passwords: {count}")

    def set_sum_files(self, num_passwords):
        """ფაილების მთლიანი რაოდენობის განახლება"""
        self.file_sum.setText(f"{num_passwords}")

    def unsafe_file_count(self, count):
        """არასაიმედო ფაილების მრიცხველის განახლება"""
        self.unsafe_file.setText(f"✖️ Unsafe files: {count}")

    def quarantine_file_count(self, count):
        """კარანტინში მყოფი ფაილების მრიცხველის განახლება"""
        self.quarantine_file.setText(f"🔏 quarantined files: {count}")

    def set_sum_threats(self, num_threats):
        """აღმოჩენილი საფრთხეების ჯამური რაოდენობის განახლება"""
        self.threat_sum.setText(f"{num_threats}")

    def password_threat(self, count):
        """საფრთხის შემცველი პაროლების ტექსტის განახლება"""
        self.weak_passwords.setText(f"❌ Unsafe passwords: {count}")

    def set_sum_duplicate(self, num_duplicate):
        """დუბლიკატი მონაცემების ჯამური რაოდენობის განახლება"""
        self.duplicate_sum.setText(f"{num_duplicate}")

    def password_duplicate(self, count):
        """დუბლიკატი პაროლების რაოდენობის განახლება"""
        self.duplicate_of_passwords.setText(f"🔑 Duplicate passwords: {count}")

    def file_duplicate(self, count):
        """დუბლიკატი ფაილების რაოდენობის განახლება"""
        self.duplicate_of_files.setText(f"🗝️ Duplicate files: {count}")