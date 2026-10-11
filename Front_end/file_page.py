import sys
import os
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QMenu,
                             QTableWidgetItem, QTreeWidgetItem, QHeaderView, QWidget, QLabel, QFileDialog)
from PyQt5.QtGui import QColor, QFont

# Fluent Widgets კომპონენტების იმპორტი
from qfluentwidgets import (TableWidget, PrimaryPushButton, SearchLineEdit,
                            ComboBox, TreeWidget, InfoBar, InfoBarPosition,
                            SubtitleLabel, FluentIcon, setTheme, Theme, ProgressBar, PushButton)


class FilePage(QWidget):
    def __init__(self, main_window):
        super().__init__(parent=main_window)
        # ობიექტის სახელისა და ფანჯრის სათაურის ინიციალიზაცია
        self.setObjectName("ფაილები")
        self.setWindowTitle("File Page")
        self.main_window = main_window

        # მონაცემთა ბაზის ფაილის სახელი
        self.db_name = "file_category.db"
        self.file_categories = []

        # მონაცემთა ბაზის შექმნა და არსებული კატეგორიების წაკითხვა
        self.init_database_and_load()

        # მთავარი ვერტიკალური განლაგების შექმნა ამ ვიჯეტისთვის
        self.main_file_layout = QVBoxLayout(self)
        self.filepage_title = QLabel(self)

        # მომხმარებლის ინტერფეისის აგება
        self.ui()

    def log_system_event(self, event_code: int, details: str = ""):
        """უსაფრთხო მეთოდი Dashboard-ის ლოგერში სტატუს კოდების გადასაცემად"""
        if self.main_window and hasattr(self.main_window, 'dashboard_page'):
            if hasattr(self.main_window.dashboard_page, 'event_log'):
                self.main_window.dashboard_page.event_log(event_code, details)

    def init_database_and_load(self):
        """ქმნის SQLite ბაზას და გამოაქვს მასში შენახული კატეგორიები"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                           CREATE TABLE IF NOT EXISTS categories
                           (
                               id
                               INTEGER
                               PRIMARY
                               KEY
                               AUTOINCREMENT,
                               name
                               TEXT
                               UNIQUE
                               NOT
                               NULL
                           )
                           """)
            conn.commit()

            cursor.execute("SELECT name FROM categories")
            rows = cursor.fetchall()
            self.file_categories = [row[0] for row in rows]

            if not self.file_categories:
                default_cats = ["Work", "Personal"]
                for cat in default_cats:
                    cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,))
                conn.commit()
                self.file_categories = default_cats

            conn.close()
        except sqlite3.Error as e:
            print(f"Database error during load: {e}")

    def ui(self):
        """მთავარი ინტერფეისის, სიდებარისა და ცხრილის მოწყობა"""
        self.setAcceptDrops(True)

        # განლაგების დაშორებების პარამეტრები
        self.main_file_layout.setSpacing(20)
        self.main_file_layout.setContentsMargins(30, 30, 30, 30)

        # მთავარი სათაურის სტილი და ტექსტი
        self.filepage_title.setText("File Page")
        self.filepage_title.setMinimumHeight(80)
        self.filepage_title.setStyleSheet('''
            font-size: 50px; 
            font-weight: bold; 
            font-family: Verdana; 
            color: white;
        ''')
        self.main_file_layout.addWidget(self.filepage_title)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # ================= 1. სიდებარის მოწყობა =================
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(10)

        sidebar_title = SubtitleLabel("Navigation")
        sidebar_title.setStyleSheet("color: white;")
        sidebar_layout.addWidget(sidebar_title)

        self.tree = TreeWidget()
        self.tree.setHeaderHidden(True)

        self.vault_root = QTreeWidgetItem(self.tree, ["My Vault"])
        self.vault_root.setIcon(0, FluentIcon.FOLDER.icon())

        self.categories_root = QTreeWidgetItem(self.tree, ["Custom Categories"])
        self.categories_root.setIcon(0, FluentIcon.TAG.icon())

        for cat in self.file_categories:
            QTreeWidgetItem(self.categories_root, [cat])

        self.quarantine_item = QTreeWidgetItem(self.tree, ["Quarantine"])
        self.quarantine_item.setIcon(0, FluentIcon.ASTERISK.icon())

        self.tree.expandAll()
        sidebar_layout.addWidget(self.tree)

        btn_layout = QHBoxLayout()
        self.add_cat_btn = PrimaryPushButton(FluentIcon.ADD, "Add")
        self.add_cat_btn.clicked.connect(self.add_new_category)

        self.delete_file_category = PushButton()
        self.delete_file_category.setText('Delete')
        self.delete_file_category.setStyleSheet(
            "QPushButton { padding: 5px; "
            "color: white; "
            "text-align: center; "
            "background-color: rgb(250, 20, 24); "
            "border: 2px solid rgba(0, 0, 0, 0.2); "
            "border-radius: 10px; }"
            "QPushButton:hover { background-color: rgb(200, 15, 20); }"
        )
        self.delete_file_category.clicked.connect(self.delete_selected_category)

        btn_layout.addWidget(self.add_cat_btn)
        btn_layout.addWidget(self.delete_file_category)
        sidebar_layout.addLayout(btn_layout)

        content_layout.addWidget(sidebar_widget, stretch=1)

        # ================= 2. მთავარი ზონის მოწყობა =================
        main_area_widget = QWidget()
        main_area_layout = QVBoxLayout(main_area_widget)
        main_area_layout.setContentsMargins(0, 0, 0, 0)
        main_area_layout.setSpacing(15)

        top_bar_layout = QHBoxLayout()
        self.search_input = SearchLineEdit()
        self.search_input.setPlaceholderText("Search files...")

        self.type_filter = ComboBox()
        self.type_filter.addItems([
            "All Files", "Documents", "Images", "Executables", "Other"
        ])

        self.upload_btn = PrimaryPushButton(FluentIcon.ADD, "Upload File")
        self.upload_btn.clicked.connect(self.handle_upload_file)

        self.scan_btn = PrimaryPushButton(FluentIcon.FOLDER, "Scan Folder")
        self.scan_btn.clicked.connect(self.handle_scan_folder)

        top_bar_layout.addWidget(self.search_input, stretch=2)
        top_bar_layout.addWidget(self.type_filter, stretch=1)
        top_bar_layout.addWidget(self.upload_btn)
        top_bar_layout.addWidget(self.scan_btn)
        main_area_layout.addLayout(top_bar_layout)

        # ცხრილის კონფიგურაცია
        self.table = TableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["File Name", "Real Type", "Size", "Upload Date", "Threat Score", "Status / Progress"])

        # ⚠️ ჩაკეტილია უჯრედების შეცვლა (Label-ებად გადაქცევა)
        self.table.setEditTriggers(QHeaderView.NoEditTriggers)

        # ⚡ სქროლბარის პოლიტიკის ჩართვა
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.verticalHeader().setDefaultSectionSize(48)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 🎨 ნაცრისფერი დიზაინი და სქროლბარის სტილიზაცია
        self.table.setStyleSheet("""
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
                font-size: 14px;
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

        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_safe_context_menu)

        # 🚀 ბევრი სატესტო სტრიქონი, რათა სქროლბარი ეგრევე დავინახოთ
        self.add_table_row("invoice.pdf", "PDF Document", "1.2 MB", "2026-06-30", 15, is_loading=False)
        self.add_table_row("payload.exe", "Executable (Fake)", "45 MB", "2026-06-29", 93, is_loading=False)
        self.add_table_row("backup.zip", "ZIP Archive", "250 MB", "2026-06-29", 10, is_loading=False)
        self.add_table_row("notes.txt", "Text Document", "4 KB", "2026-06-28", 0, is_loading=False)
        self.add_table_row("script.py", "Python File", "12 KB", "2026-06-27", 45, is_loading=False)
        self.add_table_row("image.png", "PNG Image", "3.4 MB", "2026-06-26", 5, is_loading=False)
        self.add_table_row("data.csv", "CSV Spreadsheet", "89 KB", "2026-06-25", 12, is_loading=False)
        self.add_table_row("setup.msi", "Windows Installer", "18 MB", "2026-06-24", 82, is_loading=False)
        self.add_table_row("invoice.pdf", "PDF Document", "1.2 MB", "2026-06-30", 15, is_loading=False)


        main_area_layout.addWidget(self.table)
        content_layout.addWidget(main_area_widget, stretch=4)

        self.main_file_layout.addLayout(content_layout)

    def add_table_row(self, name, real_type, size, date, score, is_loading=False):
        """ცხრილში ახალი სტრიქონის დამატება მონაცემების მიხედვით"""
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_name = QTableWidgetItem(name)
        item_type = QTableWidgetItem(real_type)
        item_size = QTableWidgetItem(size)
        item_date = QTableWidgetItem(date)

        score_item = QTableWidgetItem(f"{score}/100")

        # ფონტები უჯრედებისთვის
        cell_font = QFont()
        cell_font.setPointSize(11)

        score_font = QFont()
        score_font.setBold(True)
        score_font.setPointSize(11)

        for item in [item_name, item_type, item_size, item_date]:
            item.setForeground(QColor("#FFFFFF"))
            item.setFont(cell_font)

        if score > 75:
            score_item.setForeground(QColor("#FF4D4D"))
        else:
            score_item.setForeground(QColor("#2ECC71"))
        score_item.setFont(score_font)

        self.table.setItem(row, 0, item_name)
        self.table.setItem(row, 1, item_type)
        self.table.setItem(row, 2, item_size)
        self.table.setItem(row, 3, date_item if 'date_item' in locals() else item_date)
        self.table.setItem(row, 4, score_item)

        if is_loading:
            progress_bar = ProgressBar(self)
            progress_bar.setValue(35)
            self.table.setCellWidget(row, 5, progress_bar)
        else:
            status_item = QTableWidgetItem("Encrypted & Safe" if score < 75 else "Quarantined")
            status_item.setForeground(QColor("#aaaaaa"))
            status_item.setFont(cell_font)
            self.table.setItem(row, 5, status_item)

    def handle_upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to upload", "", "All Files (*.*)")
        if file_path:
            file_name = os.path.basename(file_path)
            try:
                file_size_bytes = os.path.getsize(file_path)
                file_size_mb = f"{file_size_bytes / (1024 * 1024):.2f} MB"
            except:
                file_size_mb = "Unknown"

            _, ext = os.path.splitext(file_name)
            file_type = f"{ext.upper().replace('.', '')} File" if ext else "Unknown File"

            self.add_table_row(file_name, file_type, file_size_mb, "Just now", 0, is_loading=True)
            self.log_system_event(201, file_name)

            InfoBar.success("Success", f"'{file_name}' successfully uploaded and encrypted.",
                            position=InfoBarPosition.BOTTOM_RIGHT, duration=4000, parent=self)

    def handle_scan_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select folder to scan")
        if folder_path:
            folder_name = os.path.basename(folder_path)
            try:
                num_files = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
            except:
                num_files = 0

            self.add_table_row(f"Folder: {folder_name}", "Directory Scan", f"{num_files} files", "Just now", 5,
                               is_loading=True)

            InfoBar.warning("Scan Started", f"Scanning directory: '{folder_name}'...",
                            position=InfoBarPosition.BOTTOM_RIGHT, duration=4000, parent=self)

    def show_safe_context_menu(self, pos):
        item = self.table.itemAt(pos)
        if item is None: return
        current_row = self.table.row(item)

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #2c2c2c; color: white; border: 1px solid #3c3c3c; padding: 5px; font-family: Segoe UI; }
            QMenu::item { padding: 6px 20px; }
            QMenu::item:selected { background-color: #3b6bb3; color: white; }
        """)

        decrypt_action = menu.addAction('Decrypt & Download')
        quarantine_action = menu.addAction('Move to Quarantine')
        menu.addSeparator()
        delete_action = menu.addAction('Delete Permanently')

        action = menu.exec_(self.table.mapToGlobal(pos))

        if action == decrypt_action:
            self.handle_decrypt(current_row)
        elif action == quarantine_action:
            self.handle_quarantine(current_row)
        elif action == delete_action:
            self.handle_delete(current_row)

    def handle_decrypt(self, row):
        if row < 0 or row >= self.table.rowCount(): return
        file_name = self.table.item(row, 0).text()
        InfoBar.success("Decryption", f"File '{file_name}' decrypted successfully.",
                        position=InfoBarPosition.BOTTOM_RIGHT, duration=3000, parent=self)

    def handle_quarantine(self, row):
        if row < 0 or row >= self.table.rowCount(): return
        file_name = self.table.item(row, 0).text()

        if not self.table.cellWidget(row, 5):
            status_item = QTableWidgetItem("Quarantined")
            status_item.setForeground(QColor("#aaaaaa"))
            self.table.setItem(row, 5, status_item)

        if self.table.item(row, 4):
            self.table.item(row, 4).setText("100/100")
            self.table.item(row, 4).setForeground(QColor("#FF4D4D"))

        self.log_system_event(402, file_name)
        InfoBar.warning("Quarantine", f"'{file_name}' transported to an isolated zone.",
                        position=InfoBarPosition.BOTTOM_RIGHT, duration=3000, parent=self)

    def handle_delete(self, row):
        if row < 0 or row >= self.table.rowCount(): return
        file_name = self.table.item(row, 0).text()
        self.table.removeRow(row)
        self.log_system_event(202, file_name)
        InfoBar.error("Delete", f"'{file_name}' deleted permanently from database.",
                      position=InfoBarPosition.BOTTOM_RIGHT, duration=3000, parent=self)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            file_name = os.path.basename(file_path)
            self.add_table_row(file_name, "Analyzing...", "Checking...", "Just now", 0, is_loading=True)
            self.log_system_event(201, file_name)
            InfoBar.success("File received", f"'{file_name}' successfully transported to scheduler.",
                            position=InfoBarPosition.BOTTOM_RIGHT, duration=4000, parent=self)

    def add_new_category(self):
        from PyQt5.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(self, 'New Category', 'Enter category name:')
        if ok and text:
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO categories (name) VALUES (?)", (text,))
                conn.commit()
                conn.close()

                self.file_categories.append(text)
                new_item = QTreeWidgetItem(self.categories_root, [text])
                new_item.setIcon(0, FluentIcon.TAG.icon())
                self.tree.expandAll()

                InfoBar.success("Success", f"Category '{text}' successfully created.",
                                position=InfoBarPosition.BOTTOM_RIGHT, duration=2000, parent=self)
            except sqlite3.IntegrityError:
                InfoBar.error("Error", "Category already exists!",
                              position=InfoBarPosition.BOTTOM_RIGHT, duration=3000, parent=self)
            except sqlite3.Error as e:
                print(f"Database error during add: {e}")

    def delete_selected_category(self):
        current_item = self.tree.currentItem()
        if not current_item:
            InfoBar.warning("Warning", "Please select a category to delete!",
                            position=InfoBarPosition.BOTTOM_RIGHT, duration=3000, parent=self)
            return

        text = current_item.text(0)
        if text in ["My Vault", "Custom Categories", "Quarantine"]:
            InfoBar.error("Error", "System category cannot be deleted!",
                          position=InfoBarPosition.BOTTOM_RIGHT, duration=3000, parent=self)
            return

        parent = current_item.parent()
        if parent:
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM categories WHERE name = ?", (text,))
                conn.commit()
                conn.close()

                if text in self.file_categories:
                    self.file_categories.remove(text)

                parent.removeChild(current_item)
                InfoBar.success("Success", f"Category '{text}' successfully deleted.",
                                position=InfoBarPosition.BOTTOM_RIGHT, duration=2500, parent=self)
            except sqlite3.Error as e:
                print(f"Database error during delete: {e}")