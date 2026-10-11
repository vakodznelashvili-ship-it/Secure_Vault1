import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QTableWidgetItem, QApplication, QHeaderView

# QFluentWidgets კომპონენტები
from qfluentwidgets import (
    LargeTitleLabel, CaptionLabel, TableWidget, PushButton,
    InfoBar, InfoBarPosition, setTheme, Theme
)


class QuarantinePage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Quarantine")
        self.setWindowTitle("Quarantine Page")
        self.main_window = main_window

        # იმიტირებული მონაცემები (ბევრი ინფორმაცია სქროლბარის დასატესტად)
        self.quarantine_files = [
            ("payment_receipt.pdf.exe", "Magic Bytes Mismatch (Executable masked as PDF)", "94/100", "2026-06-28"),
            ("unknown_script.py", "High Shannon Entropy (Potential Ransomware/Encrypted)", "81/100", "2026-06-30"),
            ("config_backup.zip", "Levenshtein Password Proximity Match", "76/100", "2026-07-01"),
            ("patch_v2.1.bat", "Malicious Command Execution Sequence Detected", "89/100", "2026-07-01"),
            ("invoice_scanned.png.scr", "Executable Script Hidden as Image Extension", "97/100", "2026-07-01"),
            ("system_dump.log", "Suspicious Data Exfiltration Dump Pattern", "72/100", "2026-07-01"),
            ("crack_tool.exe", "Known Trojan Signature Match (Database Entry #402)", "100/100", "2026-07-01")
        ]

        self.init_ui()

    def init_ui(self):
        # მთავარი ვერტიკალური განლაგება
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(35, 35, 35, 35)
        main_layout.setSpacing(15)

        # ფონტების კონფიგურაცია
        cell_font = QFont()
        cell_font.setPointSize(11)

        score_font = QFont()
        score_font.setBold(True)
        score_font.setPointSize(11)

        button_font = QFont()
        button_font.setBold(True)
        button_font.setPointSize(10)

        # 1. გვერდის მთავარი სათაური
        self.page_title = LargeTitleLabel("Threat Quarantine Zone", self)
        self.page_title.setStyleSheet("font-size: 40px; color: #ffffff; font-weight: bold;")
        main_layout.addWidget(self.page_title)

        # გვერდის მოკლე აღწერა
        self.page_desc = CaptionLabel(
            "Isolated files that triggered risk thresholds in the Threat Scoring Engine or Rule-Based Automation.",
            self)
        self.page_desc.setStyleSheet("font-size: 20px; color: #aaaaaa;")
        main_layout.addWidget(self.page_desc)

        # 2. Fluent სტილის ცხრილის შექმნა
        self.file_table = TableWidget(self)
        self.file_table.setColumnCount(5)
        self.file_table.setHorizontalHeaderLabels(
            ["File Name", "Detection Reason", "Threat Score", "Date Isolated", "Actions"])

        # კრძალავს ჩასწორებას
        self.file_table.setEditTriggers(QHeaderView.NoEditTriggers)

        # უზრუნველყოფს სქროლბარის გამოჩენას მხოლოდ მაშინ, როცა ინფორმაცია ბევრია
        self.file_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.file_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # უჯრედების სიმაღლე
        self.file_table.verticalHeader().setDefaultSectionSize(48)

        # 🎨 განახლებული ნაცრისფერი (Light Dark) სტილი + თხელი სქროლბარი
        self.file_table.setStyleSheet("""
            QTableWidget {
                background-color: #2d2d2d;
                border: 1px solid #3d3d3d;
                color: white;
                gridline-color: #3d3d3d;
                border-radius: 8px;
            }
            QTableWidget::item {
                background-color: #2d2d2d;
                color: white;
                padding-left: 10px;
            }
            QTableWidget::item:selected {
                background-color: #3b6bb3;
                color: white;
            }
            QHeaderView::section {
                background-color: #353535;
                color: #ffffff;
                padding: 10px;
                border: 1px solid #454545;
                font-size: 15px;
                font-weight: bold;
            }
            /* 🎚️ სქროლბარის ლამაზი ნაცრისფერი ვიზუალი */
            QScrollBar:vertical {
                border: none;
                background: #252525;
                width: 10px;
                margin: 0px 0px 0px 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

        # სვეტების ზომების პროპორციული გადანაწილება
        header = self.file_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

        # ცხრილის რიგების რაოდენობის განსაზღვრა
        row_count = len(self.quarantine_files)
        self.file_table.setRowCount(row_count)

        # მონაცემების ციკლით ჩაყრა ცხრილში და ღილაკების გენერაცია
        for row_idx, file_info in enumerate(self.quarantine_files):
            # File Name
            name_item = QTableWidgetItem(file_info[0])
            name_item.setFont(cell_font)
            self.file_table.setItem(row_idx, 0, name_item)

            # Detection Reason
            reason_item = QTableWidgetItem(file_info[1])
            reason_item.setFont(cell_font)
            self.file_table.setItem(row_idx, 1, reason_item)

            # Threat Score (წითელი ფერით)
            score_item = QTableWidgetItem(file_info[2])
            score_item.setForeground(QColor("#ff4d4d"))
            score_item.setFont(score_font)
            self.file_table.setItem(row_idx, 2, score_item)

            # Date Isolated
            date_item = QTableWidgetItem(file_info[3])
            date_item.setFont(cell_font)
            self.file_table.setItem(row_idx, 3, date_item)

            # მოქმედებების (Actions) კონტეინერი და ღილაკები
            action_container = QWidget()
            btn_layout = QHBoxLayout(action_container)
            btn_layout.setContentsMargins(12, 2, 12, 2)
            btn_layout.setSpacing(8)

            # Restore ღილაკი
            restore_btn = PushButton("Restore", action_container)
            restore_btn.setFixedSize(85, 30)
            restore_btn.setFont(button_font)
            restore_btn.setStyleSheet("""
                PushButton {
                    background-color: #2b579a; 
                    color: white; 
                    border-radius: 5px;
                }
                PushButton:hover {
                    background-color: #3b6bb3;
                }
            """)
            restore_btn.clicked.connect(lambda checked, r=row_idx: self.restore_file_action(r))

            # Delete ღილაკი
            delete_btn = PushButton("Delete", action_container)
            delete_btn.setFixedSize(85, 30)
            delete_btn.setFont(button_font)
            delete_btn.setStyleSheet("""
                PushButton {
                    background-color: #ff4d4d; 
                    color: white; 
                    border-radius: 5px;
                }
                PushButton:hover {
                    background-color: #ff6666;
                }
            """)
            delete_btn.clicked.connect(lambda checked, r=row_idx: self.delete_file_action(r))

            btn_layout.addWidget(restore_btn)
            btn_layout.addWidget(delete_btn)
            action_container.setLayout(btn_layout)

            # კონტეინერის დასმა Actions სვეტში
            self.file_table.setCellWidget(row_idx, 4, action_container)

        # ცხრილის მარცხენა ინდექსების დამალვა
        self.file_table.verticalHeader().setVisible(False)

        # ცხრილის დამატება მთავარ ლეაუტში
        main_layout.addWidget(self.file_table)

    def restore_file_action(self, row_index):
        file_name = self.file_table.item(row_index, 0).text()
        InfoBar.success(
            title="File Restored",
            content=f"'{file_name}' has been safely decrypted and moved back to its source location.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3500,
            parent=self
        )

    def delete_file_action(self, row_index):
        file_name = self.file_table.item(row_index, 0).text()
        InfoBar.warning(
            title="Permanently Deleted",
            content=f"'{file_name}' has been securely shredded and removed from the system storage.",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=3500,
            parent=self
        )