# PyQt5-ის ძირითადი მოდულების იმპორტი ლოგიკისთვის, ზომებისთვის და ტაიმერისთვის
from PyQt5.QtCore import Qt, QSize, QTimer
# PyQt5-ის ვიზუალური მოდულების იმპორტი ხატულებისა და შრიფტებისთვის
from PyQt5.QtGui import QIcon, QFont
# qfluentwidgets ბიბლიოთეკიდან მზა ლამაზი კომპონენტების იმპორტი
from qfluentwidgets import (FluentWindow, PrimaryPushButton, PushButton, LineEdit, PasswordLineEdit, SearchLineEdit,
                            TableWidget, MessageBox, InfoBar, FluentIcon as FIF, setCustomStyleSheet, setTheme, Theme,
                            CardWidget, SubtitleLabel, ComboBox)
# PyQt5-ის სტანდარტული ინტერფეისის ელემენტების იმპორტი
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QTableWidgetItem,
                             QFrame, QListWidget, QPushButton, QProgressBar, QMessageBox, QListWidgetItem, QInputDialog)
# მონაცემთა ბაზასთან სამუშაო ბიბლიოთეკის იმპორტი
import sqlite3

# მთავარი კლასი, რომელიც წარმოადგენს პაროლების მართვის მთლიან გვერდს
class PasswordPage(QWidget):

    # საკონსტრუქტორო მეთოდი, რომელიც ინიციალიზაციას უკეთებს გვერდს
    def __init__(self, main_window):
        # მშობელი კლასის ინიციალიზაციის გამოძახება
        super().__init__()
        # ობიექტის სახელის მინიჭება სტილებისთვის
        self.setObjectName("Password")
        # ფანჯრის სათაურის დაყენება
        self.setWindowTitle("Password Page")
        # მთავარი ფანჯრის ობიექტის შენახვა კლასის შიგნით
        self.main_window = main_window

        # მიმდინარე აქტიური ჩანაწერის ID რედაქტირებისა და წაშლის რეჟიმისთვის
        self.current_editing_id = None

        # მთლიანი გვერდის მთავარი ვერტიკალური განლაგება
        self.main_password_layout = QVBoxLayout(self)

        # ჰორიზონტალური განლაგება საძიებო და სარეგისტრაციო ბლოკების გვერდიგვერდ დასასმელად
        self.password_field_layout = QHBoxLayout()

        # მარცხენა საძიებო ბლოკის კონტეინერი (ბარათი)
        self.password_searchfield = CardWidget(self)
        # მარცხენა ბლოკის შიდა ვერტიკალური განლაგება
        self.vertical_password_search = QVBoxLayout(self.password_searchfield)
        # საძიებო ტექსტური ველი
        self.password_search = SearchLineEdit(self)
        # კატეგორიების გასაფილტრი ჩამოსაშლელი სია
        self.category = ComboBox(self)
        # გაფილტრული პაროლების საჩვენებელი სია
        self.password_list = QListWidget(self)
        # ძებნის დამწყები მთავარი ღილაკი
        self.search_button = PushButton(self)

        # მარჯვენა სარეგისტრაციო ბლოკის კონტეინერი (ბარათი)
        self.passwordfield = CardWidget(self)
        # მარჯვენა ბლოკის შიდა ვერტიკალური განლაგება
        self.vertical_password_create = QVBoxLayout(self.passwordfield)
        # მარჯვენა ბლოკის მთავარი სათაური
        self.passwordfield_title = QLabel(self)
        # სათაურის შესაყვანი ველის წარწერა
        self.name_label = QLabel(self)
        # სათაურის/სახელის შესაყვანი ტექსტური ველი
        self.name = LineEdit(self)
        # მომხმარებლის სახელის წარწერა
        self.username_label = QLabel(self)
        # მომხმარებლის სახელის შესაყვანი ტექსტური ველი
        self.username = LineEdit(self)
        # პაროლის შესაყვანი ველის წარწერა
        self.password_label = QLabel(self)
        # პაროლის შესაყვანი დაფარული ველი
        self.password = PasswordLineEdit(self)
        # კატეგორიის არჩევის წარწერა
        self.category_label = QLabel(self)
        # კატეგორიის მისანიჭებელი ჩამოსაშლელი სია
        self.password_category = ComboBox(self)
        # კატეგორიის წაშლის პატარა ღილაკი
        self.delete_category = PushButton(self)
        # პაროლის სიძლიერის პროგრეს ბარი
        self.strength_bar = QProgressBar(self)
        # პაროლის სიძლიერის პროცენტული წარწერა
        self.strength_label = QLabel(self)
        # ვებ-მისამართის ველის წარწერა
        self.url_label = QLabel(self)
        # ვებ-მისამართის შესაყვანი ტექსტური ველი
        self.url = LineEdit(self)
        # ჩანაწერის წაშლის ღილაკი
        self.delete_password_button = PushButton(self)
        # ჩანაწერის ბაზაში შენახვის/განახლების ღილაკი
        self.save_password_button = PushButton(self)
        # შემთხვევითი პაროლის გენერირების ღილაკი
        self.generate_password_button = PushButton(self)
        # ახალი ჩანაწერის დამატების ღილაკი
        self.add_password_button = PushButton(self)

        # მთლიანი გვერდის ზედა დიდი სათაურის ლეიბლი
        self.passwordpage_title = QLabel(self)

        # ვიზუალური მხარის ამწყობი მეთოდის გამოძახება
        self.UI()
        # ბაზიდან კატეგორიების ჩამომტვირთავი მეთოდის გამოძახება
        self.load_password_categories()

    # მეთოდი, რომელიც მართავს ვიჯეტების განლაგებას, ზომებსა და სტილებს
    def UI(self):
        # მთავარი განლაგების ელემენტებს შორის დაშორების დაყენება
        self.main_password_layout.setSpacing(40)
        # მთავარი განლაგების შიდა ჩარჩოდან დაშორებების დაყენება
        self.main_password_layout.setContentsMargins(30, 30, 30, 30)

        # ზედა დიდი სათაურის ტექსტის განსაზღვრა
        self.passwordpage_title.setText("Password Page")
        # ზედა სათაურის ფიქსირებული სიმაღლის დაყენება
        self.passwordpage_title.setFixedHeight(100)
        # ზედა სათაურის შრიფტის, ზომის და თეთრი ფერის სტილი
        self.passwordpage_title.setStyleSheet(
            'font-size: 60px; font-weight: bold; font-family: Verdana; padding: 5px; color: white;')

        # ზედა სათაურის დამატება მთავარ განლაგებაში
        self.main_password_layout.addWidget(self.passwordpage_title)

        # მარცხენა საძიებო ბარათის ჩასმა ქვე-განლაგებაში
        self.password_field_layout.addWidget(self.password_searchfield)
        # მარჯვენა სარეგისტრაციო ბარათის ჩასმა ქვე-განლაგებაში
        self.password_field_layout.addWidget(self.passwordfield)
        # ქვე-განლაგების შიდა ჩარჩოდან დაშორებების განსაზღვრა
        self.password_field_layout.setContentsMargins(30, 30, 30, 30)
        # ორ მთავარ ბარათს შორის ჰორიზონტალური დაშორების დაყენება
        self.password_field_layout.setSpacing(40)

        # ორი ბარათის განლაგების დამატება მთავარ ვერტიკალურ განლაგებაში
        self.main_password_layout.addLayout(self.password_field_layout)

        # საძიებო ველის ჩასმა მარცხენა კონტეინერში
        self.vertical_password_search.addWidget(self.password_search)
        # საძიებო კატეგორიის ჩასმა მარცხენა კონტეინერში
        self.vertical_password_search.addWidget(self.category)

        # ⚡ აქედან იწყება სქროლბარის და სტილის ჩამატება ⚡
        # ვერტიკალური სქროლბარის ჩართვა საჭიროებისამებრ, ხოლო ჰორიზონტალურის გამორთვა
        self.password_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.password_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # პაროლების სიის და სქროლბარის ვიზუალური სტილი (StyleSheet)
        self.password_list.setStyleSheet("""
                    QListWidget {
                        background-color: #2d2d2d;
                        border: 1px solid #3d3d3d;
                        color: white;
                        border-radius: 8px;
                        padding: 5px;
                    }
                    QListWidget::item {
                        background-color: #353535;
                        margin-bottom: 5px;
                        padding: 10px;
                        border-radius: 5px;
                        color: white;
                    }
                    QListWidget::item:hover {
                        background-color: #404040;
                    }
                    QListWidget::item:selected {
                        background-color: #3b6bb3;
                        color: white;
                    }
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
        # ⚡ სქროლბარის კოდის დასასრული ⚡

        # პაროლების სიის ჩასმა მარცხენა კონტეინერში
        self.vertical_password_search.addWidget(self.password_list)
        # ძებნის ღილაკის ჩასმა მარცხენა კონტეინერში
        self.vertical_password_search.addWidget(self.search_button)

        # სარეგისტრაციო ბლოკის სათაურის ტექსტის დასმა
        self.passwordfield_title.setText('Password record')
        # სათაურის სიმაღლის განსაზღვრა
        self.passwordfield_title.setFixedHeight(100)
        # სათაურის ვიზუალური სტილის მინიჭება
        self.passwordfield_title.setStyleSheet(
            'font-size: 45px; font-family: Verdana; font-weight: bold; color: white;')

        # საერთო ვიზუალური სტილი გვერდითა წარწერებისთვის
        label_style = 'color: white; font-weight: bold; font-family: Verdana; font-size: 25px; padding: 5px;'

        # საერთო დინამიური სტილი ძირითადი მართვის ღილაკებისთვის
        button_style = '''
                    QPushButton {{
                        font-size: 20px;
                        font-family: Verdana;
                        font-weight: bold;
                        color: white;
                        padding: 5px;
                        border-radius: 25px;
                        border: 2px solid rgba(0, 0, 0, 0.2);
                        background-color: {};
                    }}
                '''
        # საერთო სტილი ტექსტური შესაყვანი ველებისთვის
        line_edit_style = '''
                    QLineEdit {
                        font-size: 22px;
                        font-family: Verdana;
                        background-color: rgb(125, 125, 125);
                        color: white; 
                        border-radius: 10px; 
                        border: 2px solid rgb(3, 3, 3);
                        padding-left: 15px;  
                        padding-right: 15px;
                    }
                '''
        # საძიებო ველზე ტექსტური სტილის მინიჭება
        self.password_search.setStyleSheet(line_edit_style)
        # საძიებო ველში დამხმარე მინიშნების ტექსტის ჩაწერა
        self.password_search.setPlaceholderText('Search by title, password, username, category and url')
        # საძიებო კატეგორიის კომბობოქსის სიმაღლის დაყენება
        self.category.setFixedHeight(40)

        # საძიებო კატეგორიის კომბობოქსის და მისი ელემენტების სტილი
        self.category.setStyleSheet(
            "ComboBox { font-size: 15px; "
            "font-family: Verdana; "
            "font-weight: bold; "
            "background-color: rgb(130, 130, 130); "
            "border: 2px solid rgba(41, 41, 41); "
            "border-radius: 10px; "
            "color: white; } "
            "ComboBox QAbstractItemView { font-size: 18px; }")

        # სარეგისტრაციო კატეგორიის კომბობოქსის და მისი ელემენტების სტილი
        self.password_category.setStyleSheet(
            "ComboBox { font-size: 15px; "
            "font-family: Verdana; "
            "font-weight: bold; "
            "background-color: rgb(130, 130, 130); "
            "border: 2px solid rgba(41, 41, 41); "
            "border-radius: 10px; "
            "color: white; } "
            "ComboBox QAbstractItemView { font-size: 18px; }")

        # კატეგორიის წაშლის ღილაკის ფიქსირებული ზომის დაყენება
        self.delete_category.setFixedSize(40, 40)
        # წაშლის ღილაკზე ნაგვის ყუთის ხატულის დასმა
        self.delete_category.setIcon(FIF.DELETE)
        # ხატულის შიდა ზომის განსაზღვრა
        self.delete_category.setIconSize(QSize(25, 25))
        # კატეგორიის წაშლის ღილაკის წითელი სტილი და მომრგვალება
        self.delete_category.setStyleSheet(
            "QPushButton { padding: 5px; "
            "text-align: center; "
            "background-color: rgb(250, 20, 24); "
            "border: 2px solid rgba(0, 0, 0, 0.2); "
            "border-radius: 10px; }")

        # ვებ-მისამართის ველის საწყისი პროტოკოლის მინიშნება
        self.url.setPlaceholderText('https://')
        # სარეგისტრაციო კატეგორიის კომბობოქსის ზომის განსაზღვრა
        self.password_category.setFixedSize(700, 40)

        # ძებნის ღილაკის ტექსტის დაყენება
        self.search_button.setText('Search')
        # ძებნის ღილაკისთვის ლურჯი ფერის სტილის მინიჭება
        self.search_button.setStyleSheet(button_style.format('rgb(86, 125, 252)'))

        # სათაურის წარწერის ტექსტის დაყენება
        self.name_label.setText('Title / Name:')
        # სათაურის წარწერაზე სტანდარტული სტილის მინიჭება
        self.name_label.setStyleSheet(label_style)
        # სათაურის წარწერის სიმაღლის დაყენება
        self.name_label.setFixedHeight(100)
        # სათაურის ტექსტური ველის სტილის მინიჭება
        self.name.setStyleSheet(line_edit_style)
        # მომხმარებლის სახელის წარწერის ტექსტის დაყენება
        self.username_label.setText('Username:    ')
        # მომხმარებლის სახელის წარწერაზე სტილის მინიჭება
        self.username_label.setStyleSheet(label_style)
        # მომხმარებლის სახელის წარწერის სიმაღლის დაყენება
        self.username_label.setFixedHeight(100)
        # მომხმარებლის სახელის ველის სტილის მინიჭება
        self.username.setStyleSheet(line_edit_style)
        # პაროლის წარწერის ტექსტის დაყენება
        self.password_label.setText('Password:     ')
        # პაროლის წარწერაზე სტილის მინიჭება
        self.password_label.setStyleSheet(label_style)
        # პაროლის წარწერის სიმაღლის დაყენება
        self.password_label.setFixedHeight(100)
        # პაროლის შეყვანის ველის სტილის მინიჭება
        self.password.setStyleSheet(line_edit_style)
        # ვებ-მისამართის წარწერის ტექსტის დაყენება
        self.url_label.setText('URL:  ')
        # ვებ-მისამართის წარწერაზე სტილის მინიჭება
        self.url_label.setStyleSheet(label_style)
        # ვებ-მისამართის წარწერის სიმაღლის დაყენება
        self.url_label.setFixedHeight(100)
        # ვებ-მისამართის ველის სტილის მინიჭება
        self.url.setStyleSheet(line_edit_style)
        # კატეგორიის წარწერის ტექსტის დაყენება
        self.category_label.setText('Category:')
        # კატეგორიის წარწერაზე სტილის მინიჭება
        self.category_label.setStyleSheet(label_style)
        # კატეგორიის წარწერის სიმაღლის დაყენება
        self.category_label.setFixedHeight(100)
        # პაროლის სიძლიერის საწყისი ტექსტის დაყენება
        self.strength_label.setText('Password strength: 0%')
        # პაროლის სიძლიერის წარწერაზე სტილის მინიჭება
        self.strength_label.setStyleSheet(label_style)
        # პაროლის სიძლიერის წარწერის სიმაღლის დაყენება
        self.strength_label.setFixedHeight(50)

        # წაშლის ღილაკის ტექსტის დაყენება
        self.delete_password_button.setText('Delete')
        # წაშლის ღილაკისთვის მუქი წითელი ფერის მიცემა
        self.delete_password_button.setStyleSheet(button_style.format('rgb(240, 46, 46)'))
        # წაშლის ღილაკის ფიქსირებული ზომის დაყენება
        self.delete_password_button.setFixedSize(200, 50)
        # შენახვის ღილაკის ტექსტის დაყენება
        self.save_password_button.setText('Save')
        # შენახვის ღილაკისთვის ლურჯი ფერის მიცემა
        self.save_password_button.setStyleSheet(button_style.format('rgb(2, 101, 222)'))
        # შენახვის ღილაკის ფიქსირებული ზომის დაყენება
        self.save_password_button.setFixedSize(200, 50)
        # გენერაციის ღილაკის ტექსტის დაყენება
        self.generate_password_button.setText('Generate')
        # გენერაციის ღილაკისთვის მწვანე ფერის მიცემა
        self.generate_password_button.setStyleSheet(button_style.format('rgb(9, 171, 3)'))
        # გენერაციის ღილაკის ფიქსირებული ზომის დაყენება
        self.generate_password_button.setFixedSize(200, 50)
        # დამატების ღილაკის ტექსტის დაყენება
        self.add_password_button.setText('Add')
        # დამატების ღილაკისთვის ღია მწვანე ფერის მიცემა
        self.add_password_button.setStyleSheet(button_style.format('rgb(8, 212, 0)'))
        # დამატების ღილაკის ფიქსირებული ზომის დაყენება
        self.add_password_button.setFixedSize(200, 50)

        # პირველი მწკრივის ჰორიზონტალური განლაგება (სათაური)
        horizontal1 = QHBoxLayout()
        # მეორე მწკრივის ჰორიზონტალური განლაგება (მომხმარებელი)
        horizontal2 = QHBoxLayout()
        # მესამე მწკრივის ჰორიზონტალური განლაგება (პაროლი)
        horizontal3 = QHBoxLayout()
        # მეოთხე მწკრივის ჰორიზონტალური განლაგება (კატეგორია)
        horizontal4 = QHBoxLayout()
        # მეხუთე მწკრივის ჰორიზონტალური განლაგება (მისამართი)
        horizontal5 = QHBoxLayout()
        # მეექვსე მწკრივის ჰორიზონტალური განლაგება (სიმტკიცე)
        horizontal6 = QHBoxLayout()
        # მეშვიდე მწკრივის ჰორიზონტალური განლაგება (მართვის ღილაკები)
        horizontal7 = QHBoxLayout()

        # მარჯვენა ბლოკის სათაურის ზედა პოზიციონირება
        self.vertical_password_create.addWidget(self.passwordfield_title, alignment=Qt.AlignTop)
        # სათაურის წარწერის ჩასმა პირველ მწკრივში
        horizontal1.addWidget(self.name_label)
        # სათაურის ველის ჩასმა პირველ მწკრივში
        horizontal1.addWidget(self.name)
        # მომხმარებლის წარწერის ჩასმა მეორე მწკრივში
        horizontal2.addWidget(self.username_label)
        # მომხმარებლის ველის ჩასმა მეორე მწკრივში
        horizontal2.addWidget(self.username)
        # პაროლის წარწერის ჩასმა მესამე მწკრივში
        horizontal3.addWidget(self.password_label)
        # პაროლის ველის ჩასმა მესამე მწკრივში
        horizontal3.addWidget(self.password)
        # კატეგორიის წარწერის ჩასმა მეოთხე მწკრივში
        horizontal4.addWidget(self.category_label)
        # კატეგორიის სიის ჩასმა მეოთხე მწკრივში
        horizontal4.addWidget(self.password_category)
        # კატეგორიის წაშლის ღილაკის ჩასმა მეოთხე მწკრივში
        horizontal4.addWidget(self.delete_category)
        # მისამართის წარწერის ჩასმა მეხუთე მწკრივში
        horizontal5.addWidget(self.url_label)
        # მისამართის ველის ჩასმა მეხუთე მწკრივში
        horizontal5.addWidget(self.url)
        # სიმტკიცის წარწერის ჩასმა მეექვსე მწკრივში
        horizontal6.addWidget(self.strength_label)
        # პროგრეს ბარის ჩასმა მეექვსე მწკრივში
        horizontal6.addWidget(self.strength_bar)
        # წაშლის ღილაკის ჩასმა მეშვიდე მწკრივში
        horizontal7.addWidget(self.delete_password_button)
        # შენახვის ღილაკის ჩასმა მეშვიდე მწკრივში
        horizontal7.addWidget(self.save_password_button)
        # გენერაციის ღილაკის ჩასმა მეშვიდე მწკრივში
        horizontal7.addWidget(self.generate_password_button)
        # დამატების ღილაკის ჩასმა მეშვიდე მწკრივში
        horizontal7.addWidget(self.add_password_button)

        # ქვედა ღილაკებს შორის დაშორების განსაზღვრა
        horizontal7.setSpacing(20)
        # ქვედა ღილაკების მწკრივის შიდა ჩარჩოდან დაშორება
        horizontal7.setContentsMargins(20, 20, 20, 20)

        # პირველი მწკრივის ჩამატება მარჯვენა ბლოკის ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal1)
        # მეორე მწკრივის ჩამატება ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal2)
        # მესამე მწკრივის ჩამატება ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal3)
        # მეოთხე მწკრივის ჩამატება ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal4)
        # მეხუთე მწკრივის ჩამატება ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal5)
        # მეექვსე მწკრივის ჩამატება ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal6)
        # მეშვიდე მწკრივის ჩამატება ვერტიკალურ განლაგებაში
        self.vertical_password_create.addLayout(horizontal7)

        # კატეგორიის არჩევის შეცვლის სიგნალის დაკავშირება მეთოდთან
        self.password_category.currentIndexChanged.connect(self.on_category_selection_changed)
        # კატეგორიის წაშლის ღილაკზე დაჭერის სიგნალის დაკავშირება მეთოდთან
        self.delete_category.clicked.connect(self.delete_category_onclick)
        # პაროლის დამატების ღილაკზე დაჭერის სიგნალის დაკავშირება მეთოდთან
        self.add_password_button.clicked.connect(self.add_button)
        # პაროლის გენერაციის ღილაკზე დაჭერის სიგნალის დაკავშირება მეთოდთან
        self.generate_password_button.clicked.connect(self.generate_password)
        # პაროლის შეცვლის/შენახვის ღილაკზე დაჭერის სიგნალის დაკავშირება მეთოდთან
        self.save_password_button.clicked.connect(self.save_button)
        # პაროლის წაშლის ღილაკზე დაჭერის სიგნალის დაკავშირება მეთოდთან
        self.delete_password_button.clicked.connect(self.delete_button)

        # პაროლის ველში ტექსტის ყოველი შეცვლისას სიძლიერის ბარის განახლება 90 ქულით
        self.password.textChanged.connect(lambda text: self.update_strength_display(90))
        # ძებნის ღილაკზე დაჭერის სიგნალის დაკავშირება ძებნის მეთოდთან
        self.search_button.clicked.connect(self.search_passwords)

    # მეთოდი, რომელიც ირთვება კატეგორიის სიიდან ახალი ელემენტის არჩევისას
    def on_category_selection_changed(self, index):
        # ვამოწმებთ, აირჩია თუ არა მომხმარებელმა ახალი კატეგორიის დამატების პუნქტი
        if self.password_category.currentText() == 'Add categories':

            # ახალი შესაყვანი დიალოგური ფანჯრის ობიექტის შექმნა
            dialog = QInputDialog(None)
            dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
            # დიალოგური ფანჯრის სათაურის დაყენება
            dialog.setWindowTitle("Adding a new category")
            # დიალოგურ ფანჯარაში შიდა წარწერის ტექსტის დასმა
            dialog.setLabelText("Please choose a new category name:")

            # დიალოგური ფანჯრის ელემენტების მუქი ვიზუალური სტილის გაწერა
            dialog.setStyleSheet("""
                QInputDialog {
                    background-color: #2b2b2b;
                }
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-family: "Segoe UI", "Arial";
                }
                QLineEdit {
                    background-color: #3b3b3b;
                    color: #ffffff;
                    border: 2px solid #0078d4;
                    border-radius: 5px;
                    padding: 6px;
                    font-size: 14px;
                }
                QPushButton {
                    background-color: #0078d4;
                    color: white;
                    border-radius: 4px;
                    min-width: 80px;
                    min-height: 28px;
                    font-weight: bold;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #106ebe;
                }
                QPushButton:pressed {
                    background-color: #005a9e;
                }
            """)

            # დიალოგური ფანჯრის საწყისი ზომების განსაზღვრა
            dialog.resize(400, 180)

            # ფანჯრის ჩვენება და იმის შემოწმება, დააჭირა თუ არა მომხმარებელმა დასტურის ღილაკს
            if dialog.exec_() == QInputDialog.Accepted:
                # შესაყვანი ველიდან ტექსტის აღება და ცარიელი ადგილების ჩამოჭრა
                text = QInputDialog()

                # ვამოწმებთ, რომ ტექსტი არ იყოს ცარიელი
                if text:
                    # ჩაწერილი ტექსტის შენახვა ახალ ცვლადში
                    new_cat = text
                    # კატეგორიების მონაცემთა ბაზასთან კავშირის დამყარება
                    conn = sqlite3.connect("category.db")
                    # კურსორის ობიექტის შექმნა ბრძანებების შესასრულებლად
                    cursor = conn.cursor()
                    try:
                        # ახალი კატეგორიის ბაზაში ჩამატება, თუ ის უკვე არ არსებობს
                        cursor.execute('INSERT OR IGNORE INTO password_category(name) VALUES(?)', (new_cat,))
                        # ცვლილებების საბოლოოდ შენახვა ბაზაში
                        conn.commit()
                        # წარმატებული ოპერაციის დაპრინტვა კონსოლში
                        print(f"წარმატებით დაემატა: {new_cat}")
                    except Exception as e:
                        # შეცდომის შემთხვევაში მისი ტექსტის კონსოლში გამოტანა
                        print(f"Error adding category: {e}")
                    finally:
                        # კურსორის მუშაობის დასრულება
                        cursor.close()
                        # ბაზასთან კავშირის გაწყვეტა
                        conn.close()

                    # კატეგორიის კომბობოქსის სიგნალების დროებითი დაბლოკვა რეკურსიის თავიდან ასაცილებლად
                    self.password_category.blockSignals(True)
                    # კატეგორიების სიის ხელახალი ჩატვირთვა ბაზიდან განახლებისთვის
                    self.load_password_categories()

                    # ახლად დამატებული კატეგორიის ინდექსის მოძებნა სიაში
                    new_index = self.password_category.findText(new_cat)
                    # თუ კატეგორია იპოვა, ავტომატურად მასზე გადართვა
                    if new_index != -1:
                        self.password_category.setCurrentIndex(new_index)
                    else:
                        # თუ ვერ იპოვა, პირველ ელემენტზე გადართვა
                        self.password_category.setCurrentIndex(0)
                    # სიგნალების ბლოკირების მოხსნა
                    self.password_category.blockSignals(False)
                else:
                    # თუ მომხმარებელმა ცარიელი ველი დაადასტურა, სიგნალების ბლოკირება
                    self.password_category.blockSignals(True)
                    # საწყის ელემენტზე დაბრუნება
                    self.password_category.setCurrentIndex(0)
                    # ბლოკირების მოხსნა
                    self.password_category.blockSignals(False)
            else:
                # თუ მომხმარებელმა უარი თქვა ფანჯარაზე, სიგნალების ბლოკირება
                self.password_category.blockSignals(True)
                # საწყის ელემენტზე დაბრუნება
                self.password_category.setCurrentIndex(0)
                # ბლოკირების მოხსნა
                self.password_category.blockSignals(False)

    # მეთოდი, რომელიც მუშაობს კატეგორიის წაშლის ღილაკზე დაჭერისას
    def delete_category_onclick(self):
        # უცვლელი სისტემური კატეგორიების სახელების განსაზღვრა
        forbidden_category = ('All categories', 'Add categories', 'Other')
        # მიმდინარე არჩეული კატეგორიის ტექსტის აღება
        category_for_delete = self.password_category.currentText()
        # მიმდინარე არჩეული კატეგორიის ინდექსის აღება
        current_index = self.password_category.currentIndex()

        # ვამოწმებთ, არის თუ არა არჩეული კატეგორია სისტემურ სიურპრიზებში ან არის თუ არა საერთოდ ცარიელი
        if category_for_delete in forbidden_category or current_index == -1:
            # საინფორმაციო გაფრთხილების ფანჯრის შექმნა
            warn_msg = QMessageBox(None)
            warn_msg.setWindowFlags(warn_msg.windowFlags() | Qt.WindowStaysOnTopHint)
            # ფანჯრის ხატულის დაყენება გაფრთხილების რეჟიმზე
            warn_msg.setIcon(QMessageBox.Warning)
            # გაფრთხილების ფანჯრის სათაურის მინიჭება
            warn_msg.setWindowTitle("Warning")
            # გაფრთხილების ძირითადი ტექსტის გაწერა
            warn_msg.setText("This item cannot be deleted!")
            # მხოლოდ დასტურის ღილაკის დაყენება ფანჯარაში
            warn_msg.setStandardButtons(QMessageBox.Ok)

            # გაფრთხილების ფანჯრის მუქი დიზაინის სტილის მინიჭება
            warn_msg.setStyleSheet("""
                QMessageBox { background-color: #2b2b2b; }
                QLabel { color: #ffffff; 
                font-size: 14px; 
                min-width: 250px; }
                QPushButton { background-color: #555555; 
                color: white; 
                border-radius: 4px; 
                min-width: 70px; 
                min-height: 26px; 
                font-weight: bold; }
                QPushButton:hover { background-color: #444444; }
            """)
            # გაფრთხილების ფანჯრის ეკრანზე ჩვენება და პროცესის შეჩერება
            warn_msg.exec_()
            # მეთოდიდან ნაადრევი გამოსვლა, რადგან წაშლა აკრძალულია
            return

        # წაშლის დადასტურების საძიებო შეკითხვის ფანჯრის შექმნა
        msg = QMessageBox(None)
        msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
        # კითხვის ხატულის მინიჭება ფანჯარაზე
        msg.setIcon(QMessageBox.Question)
        # ფანჯრის სათაურის ტექსტის დაყენება
        msg.setWindowTitle("Delete Category")
        # კითხვის შინაარსის გაწერა კონკრეტული კატეგორიის სახელის მითითებით
        msg.setText(f"Are you sure you want to delete the category: '{category_for_delete}'?\n"
                    "This will not delete the passwords inside it.")
        # კი და არა ღილაკების დამატება არჩევანისთვის
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # დადასტურების ფანჯრის მუქი ვიზუალური გაფორმება
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-family: "Segoe UI", "Arial";
                min-width: 320px;
            }
            QPushButton {
                background-color: #d9534f;
                color: white;
                border-radius: 4px;
                min-width: 70px;
                min-height: 26px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
            QPushButton[text="&No"] {
                background-color: #555555;
            }
            QPushButton[text="&No"]:hover {
                background-color: #444444;
            }
        """)

        # ფანჯრის გამოძახება და მომხმარებლის მიერ დაჭერილი ღილაკის შედეგის შენახვა
        result = msg.exec_()

        # ვამოწმებთ, დააჭირა თუ არა მომხმარებელმა თანხმობის ღილაკს
        if result == QMessageBox.Yes:
            # მონაცემთა ბაზასთან კავშირის გახსნა
            conn = sqlite3.connect("category.db")
            # ბრძანებების კურსორის შექმნა
            cursor = conn.cursor()
            try:
                # კატეგორიის სახელის გასუფთავება ზედმეტი ცარიელი ჰარებისგან
                clean_name = category_for_delete.strip()
                # ბაზიდან შესაბამისი სახელით კატეგორიის წაშლის ბრძანების გაშვება
                cursor.execute('DELETE FROM password_category WHERE name = ?', (clean_name,))
                # ცვლილებების შენახვა მონაცემთა ბაზის ფაილში
                conn.commit()
                # კონსოლში წაშლის წარმატებით დასრულების შეტყობინება
                print(f"წარმატებით წაიშალა ბაზიდან: {clean_name}")

                # ორივე კომბობოქსის სიგნალების დაბლოკვა ვიზუალური წაშლისას
                self.password_category.blockSignals(True)
                self.category.blockSignals(True)

                # მიმდინარე ელემენტის წაშლა მარჯვენა სარეგისტრაციო სიიდან
                self.password_category.removeItem(current_index)
                # მარჯვენა სიის საწყის პოზიციაზე დაბრუნება
                self.password_category.setCurrentIndex(0)

                # წაშლილი კატეგორიის ინდექსის მოძებნა მარცხენა საძიებო სიაში
                other_combo_index = self.category.findText(category_for_delete)
                # თუ მარცხენა სიაშიც იპოვა ეს ელემენტი, მისი იქიდანაც წაშლა
                if other_combo_index != -1:
                    self.category.removeItem(other_combo_index)
                # მარცხენა სიის პირველ ელემენტზე გადაყვანა
                self.category.setCurrentIndex(0)

                # ორივე კომბობოქსის სიგნალების ბლოკირების მოხსნა
                self.password_category.blockSignals(False)
                self.category.blockSignals(False)

            except Exception as e:
                # შესაძლო შეცდომის გამოტანა კონსოლში
                print(f"Error deleting category: {e}")
            finally:
                # კურსორის დახურვა
                cursor.close()
                # ბაზის კავშირის დახურვა
                conn.close()

    # მეთოდი ბაზიდან ყველა შენახული კატეგორიის სიებში ჩამოსატვირთად
    def load_password_categories(self):
        # სიგნალების ბლოკირება, რომ ჩატვირთვისას არ გამოიწვიოს ავტომატური რეაქციები
        self.password_category.blockSignals(True)
        # მარჯვენა კომბობოქსის ელემენტების სრული გაწმენდა
        self.password_category.clear()
        # მარცხენა კომბობოქსის ელემენტების სრული გაწმენდა
        self.category.clear()
        # მარჯვენა სიის საწყის ელემენტად სხვა კატეგორიის დამატება
        self.password_category.addItem('Other')
        # მარცხენა სიის საწყის ელემენტად ყველა კატეგორიის ფილტრის დამატება
        self.category.addItem('All categories')

        try:
            # ბაზის ფაილთან კავშირის დამყარება
            conn = sqlite3.connect("category.db")
            # ბრძანებების კურსორის შექმნა
            cursor = conn.cursor()
            # კატეგორიების ცხრილიდან ყველა სახელის წაკითხვის ბრძანება
            cursor.execute('SELECT name FROM password_category')
            # ყველა წაკითხული მწკრივის ერთიან მასივში ამოღება
            rows = cursor.fetchall()

            # კურსორის უსაფრთხოდ დახურვა მონაცემების წაკითხვისთანავე
            cursor.close()
            # ბაზასთან კავშირის დახურვა
            conn.close()

            # წაკითხული მასივის ციკლით გავლა და თითოეული ელემენტის სიებში ჩამატება
            for row in rows:
                # ელემენტის დამატება მარჯვენა სარეგისტრაციო კომბობოქსში
                self.password_category.addItem(row[0])
                # ელემენტის დამატება მარცხენა საძიებო კომბობოქსში
                self.category.addItem(row[0])

        except Exception as e:
            # ბაზიდან წაკითხვის შეცდომის დაპრინტვა
            print(f"Error loading categories: {e}")
        # მარცხენა სიის ბოლოში სხვა კატეგორიის ელემენტის მიბმა
        self.category.addItem('Other')
        # მარჯვენა სიის ბოლოში ახალი კატეგორიის დამატების ფუნქციური პუნქტის მიბმა
        self.password_category.addItem('Add categories')
        # მარჯვენა კომბობოქსისთვის სიგნალების ბლოკირების მოხსნა
        self.password_category.blockSignals(False)

    # მეთოდი, რომელიც მუშაობს ახალი პაროლის დამატების ღილაკზე დაჭერისას
    def add_button(self):
        # სათაურის ტექსტის აღება და გვერდითი ცარიელი ადგილების მოცილება
        title = self.name.text().strip()
        # მომხმარებლის სახელის აღება და გასუფთავება
        username = self.username.text().strip()
        # შეყვანილი პაროლის ტექსტის აღება და გასუფთავება
        password = self.password.text().strip()
        # მიმდინარე არჩეული კატეგორიის ტექსტის წაკითხვა
        category = self.password_category.currentText()
        # ვებ-მისამართის ტექსტის წაკითხვა და გასუფთავება
        url = self.url.text().strip()

        # უსაფრთხოების შემოწმება: თუ სათაური ან პაროლი ცარიელია, ოპერაცია წყდება
        if not title or not password:
            return

        # სატესტო შეტყობინება იმის საჩვენებლად, რომ მონაცემები მზადაა ბაზისთვის
        print(f"გადაეცემა პარტნიორს დასამატებლად: {title}")

        # ველების გასუფთავების შიდა მეთოდის გამოძახება წარმატებული დამატების მერე
        self.clear_fields()
        # სიის ავტომატური განახლება ცვლილების ასასახად
        self.search_passwords()

    # მეთოდი შემთხვევითი პაროლის შესაქმნელად და ველში ჩასასმელად
    def generate_password(self):
        # სატესტო გენერირებული პაროლის სტრიქონი პარტნიორის ლოგიკის ჩასმამდე
        mock_generated = "Generated_Password_2026"
        # გენერირებული ტექსტის პირდაპირ ჩასმა პაროლის შესაყვან ველში
        self.password.setText(mock_generated)

    # მეთოდი, რომელიც მუშაობს შენახვის/განახლების ღილაკზე დაჭერისას
    def save_button(self):
        self.main_window.dashboard_page.event_log(102, f"Name: {self.name.text()}, Username: {self.username.text()}, Password: {self.password.text()}")
        # ვამოწმებთ, გვაქვს თუ არა არჩეული კონკრეტული ID რედაქტირებისთვის
        if self.current_editing_id is None:
            # შეტყობინება კონსოლში, თუ მომხმარებელი ცდილობს ჰაერზე შენახვას
            print("არცერთი ჩანაწერი არ არის არჩეული განახლებისთვის")
            return

        # განახლებული სათაურის წაკითხვა ველიდან
        title = self.name.text().strip()
        # განახლებული მომხმარებლის სახელის წაკითხვა ველიდან
        username = self.username.text().strip()
        # განახლებული პაროლის მნიშვნელობის წაკითხვა ველიდან
        password = self.password.text().strip()
        # განახლებული კატეგორიის მნიშვნელობის წაკითხვა ველიდან
        category = self.password_category.currentText()
        # განახლებული ვებ-მისამართის წაკითხვა ველიდან
        url = self.url.text().strip()

        # შეტყობინება, რომელიც მიუთითებს თუ რომელი ID-ს განახლება უნდა მოხდეს SQL-ით
        print(f"გადაეცემა პარტნიორს განახლებისთვის ID: {self.current_editing_id}")

        # ღილაკის ტექსტის საწყის მდგომარეობაზე "Save"-ზე დაბრუნება
        self.save_password_button.setText("Save")
        # მიმდინარე აქტიური ID-ს ხელახლა განულება
        self.current_editing_id = None
        # ტექსტური ველების სრული გაწმენდა ფორმაში
        self.clear_fields()
        # სიის მონაცემების ხელახალი ძებნა-განახლება ეკრანზე
        self.search_passwords()

    # მეთოდი, რომელიც მუშაობს ჩანაწერის წაშლის ღილაკზე დაჭერისას
    def delete_button(self):
        self.main_window.dashboard_page.event_log(103, f"{self.name.text()} deleted ")
        # ვამოწმებთ, გვაქვს თუ არა მონიშნული რომელიმე ჩანაწერი წასაშლელად
        if self.current_editing_id is None:
            # გაფრთხილება კონსოლში, თუ არცერთი ID არ არის აქტიური
            print("არცერთი ჩანაწერი არ არის არჩეული წასაშლელად")
            return

        # სატესტო შეტყობინება პარტნიორისთვის, რომ წაშალოს ეს ID ბაზიდან
        print(f"გადაეცემა პარტნიორს წასაშლელად ID: {self.current_editing_id}")

        # მთავარი ღილაკის ტექსტის საწყის პოზიციაზე დაბრუნება
        self.save_password_button.setText("Save")
        # აქტიური ID ცვლადის მნიშვნელობის განულება
        self.current_editing_id = None
        # ფორმის შესაყვანი ველების სრული გასუფთავება
        self.clear_fields()
        # ეკრანზე პაროლების სიის ავტომატური გადახატვა-განახლება
        self.search_passwords()

    # დამხმარე მეთოდი ფორმაში არსებული ყველა ტექსტური ველის ერთდროულად გასასუფთავებლად
    def clear_fields(self):
        # სათაურის ველის ტექსტის წაშლა
        self.name.clear()
        # მომხმარებლის სახელის ველის ტექსტის წაშლა
        self.username.clear()
        # პაროლის ველის ტექსტის წაშლა
        self.password.clear()
        # ვებ-მისამართის ველის ტექსტის წაშლა
        self.url.clear()
        # თუ კომბობოქსში ელემენტები არსებობს, პირველ საწყის პოზიციაზე გადაყვანა
        if self.password_category.count() > 0:
            self.password_category.setCurrentIndex(0)

    # მეთოდი, რომელიც მართავს პროგრეს ბარის პროცენტებსა და ფერებს მიღებული ქულის მიხედვით
    def update_strength_display(self, score):
        try:
            # მიღებული მნიშვნელობის მთელ რიცხვში კონვერტაცია
            score = int(score)
            # ქულის დიაპაზონის იძულებითი შენარჩუნება 0-დან 100 პროცენტამდე
            score = max(0, min(score, 100))

            # პროგრეს ბარის მიმდინარე მნიშვნელობის დასმა
            self.strength_bar.setValue(score)
            # პროცენტული წარწერის განახლება მიღებული ქულით
            self.strength_label.setText(f"Password strength: {score}%")

            # ფერის შერჩევა: თუ ქულა 40-ზე ნაკლებია, პაროლი სუსტია და ფერი ხდება წითელი
            if score < 40:
                color = "#ff4d4d"
            # თუ ქულა 40-დან 75-მდეა, პაროლი საშუალოა და ფერი ხდება ყვითელი
            elif score < 75:
                color = "#ffaa00"
            # თუ ქულა 75-ზე მეტია, პაროლი ძლიერია და ფერი ხდება მწვანე
            else:
                color = "#2ecc71"

            # პროგრეს ბარის ვიზუალური სტილისა და მიმდინარე დინამიური ფერის მინიჭება
            self.strength_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 2px solid #333333;
                    border-radius: 5px;
                    background-color: #2b2b2b;
                    text-align: center;
                    color: transparent;
                    height: 15px;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 3px;
                }}
            """)
        except Exception as e:
            # შეცდომის გამოტანა კონსოლში პროგრესის გათვლისას
            print(f"Error updating strength display: {e}")

    # მეთოდი, რომელიც კითხულობს საძიებო ველებს და ფილტრავს მონაცემებს სიისთვის
    def search_passwords(self):
        # საძიებო ტექსტურ ველში არსებული ჩანაწერის წაკითხვა და ჰარების მოცილება
        search_text = self.password_search.text().strip()
        # საძიებო ფილტრის მიმდინარე კატეგორიის წაკითხვა
        selected_category = self.category.currentText()

        # კონსოლში მიმდინარე ძებნის პარამეტრების ინფორმაციული პრინტი
        print(f"ძებნა... ტექსტი: '{search_text}', კატეგორია: '{selected_category}'")

        # დროებითი სატესტო მონაცემების მასივი რეალური მონაცემთა ბაზის ჩანაცვლებამდე
        mock_data = [
            (1, "Facebook", "giorgi_fb", "Pass123!", "https://facebook.com", "Social Media"),
            (2, "Gmail", "giorgi.work", "Mail456$", "https://gmail.com", "Work"),
            (3, "Netflix", "family_acc", "Net789#", "https://netflix.com", "Other")
        ]

        # ცარიელი მასივი მხოლოდ გაფილტრული შედეგების შესანახად
        filtered_data = []
        # სატესტო მონაცემების სათითაოდ შემოწმება ციკლის მეშვეობით
        for row in mock_data:
            # მიმდინარე მწკრივის სათაურის ამოღება
            title = row[1]
            # ვამოწმებთ, თუ საძიებო ველი ცარიელია, ან ჩაწერილი ტექსტი ემთხვევა სათაურს
            if not search_text or search_text.lower() in title.lower():
                # კრიტერიუმების შესაბამისი მწკრივის დამატება გაფილტრულ მასივში
                filtered_data.append(row)

        # გაფილტრული მონაცემების გადაცემა ეკრანზე დასახატი მეთოდისთვის
        self.display_passwords(filtered_data)

    # მეთოდი, რომელიც ასუფთავებს QListWidget-ს და ავსებს მას ახალი ბარათებით
    def display_passwords(self, password_rows):
        # სიის ვიზუალური ელემენტების სრული გაწმენდა ძველი შინაარსისგან
        self.password_list.clear()
        # სიის ელემენტის მუქი ფონური ფერის და ჩარჩოს მოცილების სტილი
        self.password_list.setStyleSheet("QListWidget { background-color: #1e1e1e; border: none; }")

        # გადმოცემული მწკრივების სათითაოდ დამუშავება ციკლში
        for row in password_rows:
            # ელემენტების ინდივიდუალური ცვლადების ამოღება მწკრივიდან
            p_id = row[0]
            title = row[1]
            username = row[2]
            password = row[3]
            url = row[4]
            category = row[5]

            # QListWidget-ის ახალი სტანდარტული ცარიელი ელემენტის შექმნა
            item = QListWidgetItem(self.password_list)
            # ჩვენი სპეციალური მწკრივის ვიჯეტის შექმნა და მშობელი კლასის (self) გადაცემა
            row_widget = PasswordRowWidget(p_id, title, username, password, url, category, self)

            # სიის ელემენტისთვის ჩვენი ვიჯეტის შესაბამისი ოპტიმალური ზომის მინიჭება
            item.setSizeHint(row_widget.sizeHint())
            # ცარიელ სტანდარტულ ელემენტში ჩვენი ლამაზი მწკრივის ვიჯეტის ჩასმა
            self.password_list.setItemWidget(item, row_widget)

    # მეთოდი, რომელიც ირთვება რომელიმე ბარათზე "Edit" ღილაკის დაჭერისას
    def open_edit_mode(self, p_id, title, username, password, url, category):
        # მარჯვენა ბლოკის ფორმისთვის მიმდინარე აქტიური სარედაქციო ID-ს დამახსოვრება
        self.current_editing_id = p_id

        # მარჯვენა ბლოკის სათაურის ველში ბარათის სათაურის ჩაწერა
        self.name.setText(title)
        # მომხმარებლის სახელის ველში ბარათის იუზერნეიმის ჩაწერა
        self.username.setText(username)
        # პაროლის ველში შესაბამისი პაროლის ტექსტის ჩაწერა
        self.password.setText(password)
        # ვებ-მისამართის ველში ბარათის ლინკის ჩაწერა
        self.url.setText(url)

        # კომბობოქსში შესაბამისი კატეგორიის ტექსტის პოზიციის მოძებნა
        cat_index = self.password_category.findText(category)
        # თუ კატეგორია სიაში იპოვა, კომბობოქსის მასზე გადართვა
        if cat_index != -1:
            self.password_category.setCurrentIndex(cat_index)

        # შენახვის ღილაკისთვის ტექსტის შეცვლა, რათა მივანიშნოთ რედაქტირებაზე
        self.save_password_button.setText("Update Password")


# ცალკეული დამოუკიდებელი კლასი სიაში თითოეული პაროლის მწკრივის ვიზუალის სამართავად
class PasswordRowWidget(QWidget):
    # მწკრივის ვიჯეტის საკონსტრუქტორო მეთოდი საჭირო არგუმენტების მისაღებად
    def __init__(self, password_id, title, username, password, url, category, main_app_parent):
        # მშობელი კლასის ინიციალიზაცია
        super().__init__()
        # ჩანაწერის უნიკალური ID-ს შენახვა ობიექტის მეხსიერებაში
        self.password_id = password_id
        # ჩანაწერის სათაურის შენახვა მეხსიერებაში
        self.title = title
        # მომხმარებლის სახელის შენახვა მეხსიერებაში
        self.username = username
        # უსაფრთხო პაროლის ტექსტის შენახვა მეხსიერებაში
        self.password = password
        # ვებ-გვერდის მისამართის შენახვა მეხსიერებაში
        self.url = url
        # კატეგორიის დასახელების შენახვა მეხსიერებაში
        self.category = category
        # მთავარ PasswordPage კლასთან დამაკავშირებელი ხიდის შენახვა
        self.main_app = main_app_parent

        # მწკრივისთვის ფიქსირებული სიმაღლის დაყენება, რომ სიაში ლამაზად ჩაჯდეს
        self.setFixedHeight(55)

        # მწკრივის შიდა ელემენტების ჰორიზონტალური განლაგება
        layout = QHBoxLayout(self)
        # ელემენტების ჩარჩოდან შიდა დაშორებების განსაზღვრა
        layout.setContentsMargins(15, 5, 15, 5)

        # საჩვენებელი წარწერის შექმნა, სადაც სათაური მუქია, ხოლო იუზერნეიმი ნაცრისფერი
        self.info_label = QLabel(f"<b><span style='color: white; font-size: 14px;'>{self.title}</span></b> "
                                 f"<span style='color: #888888;'>({self.username})</span>")
        # წარწერისთვის ვერდანას შრიფტის სტილის მინიჭება
        self.info_label.setStyleSheet("font-family: Verdana;")
        # საინფორმაციო წარწერის ჩამატება მწკრივის განლაგებაში
        layout.addWidget(self.info_label)

        # ზამბარის (Stretch) დამატება ტექსტის მარცხნივ და ღილაკების მარჯვნივ გადასაწევად
        layout.addStretch()

        # პაროლის კოპირების ღილაკის ობიექტის შექმნა
        self.copy_btn = QPushButton("Copy")
        # კოპირების ღილაკის ფიქსირებული ზომების დაყენება
        self.copy_btn.setFixedSize(65, 30)
        # კოპირების ღილაკის ლურჯი სტილის გაწერა მაუსის მიტანის ეფექტით
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(2, 101, 222);
                color: white;
                border-radius: 6px;
                font-family: Verdana;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgb(0, 80, 180); }
        """)
        # კოპირების ღილაკზე დაჭერისას ტაიმერისა და კოპირების მეთოდის გამოძახება
        self.copy_btn.clicked.connect(self.start_copy_countdown)
        # კოპირების ღილაკის ჩასმა მწკრივის განლაგების ბოლოში
        layout.addWidget(self.copy_btn)

        # რედაქტირების ღილაკის ობიექტის შექმნა
        self.edit_btn = QPushButton("Edit")
        # რედაქტირების ღილაკის ფიქსირებული ზომების დაყენება
        self.edit_btn.setFixedSize(65, 30)
        # რედაქტირების ღილაკის ნაცრისფერი სტილის გაწერა მაუსის მიტანის ეფექტით
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(125, 125, 125);
                color: white;
                border-radius: 6px;
                font-family: Verdana;
                font-weight: bold;
            }
            QPushButton:hover { background-color: rgb(100, 100, 100); }
        """)
        # რედაქტირების ღილაკზე კლიკის დაკავშირება შესაბამის შიდა მეთოდთან
        self.edit_btn.clicked.connect(self.edit_clicked)
        # რედაქტირების ღილაკის ჩასმა მწკრივის განლაგების ბოლოში
        layout.addWidget(self.edit_btn)

        # უკუათვლის ტაიმერის ობიექტის შექმნა მიმდინარე ვიჯეტისთვის
        self.countdown_timer = QTimer(self)
        # ტაიმერის ყოველ ინტერვალზე წამების განახლების მეთოდის მიბმა
        self.countdown_timer.timeout.connect(self.update_countdown)
        # საწყისი წამების რაოდენობის განსაზღვრა უსაფრთხოებისთვის (30 წამი)
        self.seconds_remaining = 30

    # მეთოდი, რომელიც აკოპირებს პაროლს და რთავს ტაიმერს
    def start_copy_countdown(self):
        try:
            # თუ main_app-ს გამოატანე password_page, მაშინ main_window იქნება ასე:
            if hasattr(self.main_app, 'main_window') and self.main_app.main_window:
                self.main_app.main_window.dashboard_page.event_log(106, f"Name: {self.title}")
        except Exception as e:
            print(f"Logging error: {e}")

        # ოპერაციული სისტემის გაცვლის ბუფერის (კლიპბორდის) ობიექტის აღება
        clipboard = QApplication.clipboard()
        # ბარათის რეალური პაროლის ტექსტის კოპირება სისტემურ მეხსიერებაში
        clipboard.setText(self.password)

        # წამების მრიცხველის ხელახლა დაყენება 30-ზე
        self.seconds_remaining = 30
        # კოპირების ღილაკის დროებითი გათიშვა, რომ ზედმეტად ბევრჯერ არ დააჭირონ
        self.copy_btn.setEnabled(False)
        # ღილაკის ტექსტად მიმდინარე დარჩენილი წამების ჩვენება
        self.copy_btn.setText(f"{self.seconds_remaining}s")
        # ტაიმერის გაშვება ყოველ 1000 მილიწამში (ანუ 1 წამში) ერთხელ
        self.countdown_timer.start(1000)

    # მეთოდი, რომელიც მუშაობს ტაიმერის ყოველ წამზე და ასუფთავებს ბუფერს ბოლოში
    def update_countdown(self):
        # დარჩენილი წამების რაოდენობის ერთით შემცირება
        self.seconds_remaining -= 1
        # ვამოწმებთ, დარჩა თუ არა კიდევ დრო ათვლისთვის
        if self.seconds_remaining > 0:
            # ღილაკზე მიმდინარე წამების განახლებული ვიზუალიზაცია
            self.copy_btn.setText(f"{self.seconds_remaining}s")
        else:
            # დროის ამოწურვისას ტაიმერის მუშაობის სრული გაჩერება
            self.countdown_timer.stop()
            # გაცვლის ბუფერის ობიექტის ხელახლა აღება
            clipboard = QApplication.clipboard()
            # უსაფრთხოების შემოწმება: იშლება მხოლოდ მაშინ, თუ ბუფერში ისევ ეს პაროლი დევს
            if clipboard.text() == self.password:
                # ბუფერის სრული გასუფთავება უსაფრთხოების მიზნით
                clipboard.clear()
            # კოპირების ღილაკის ხელახლა გააქტიურება ახალი ოპერაციებისთვის
            self.copy_btn.setEnabled(True)
            # ღილაკის ტექსტის საწყის "Copy" მნიშვნელობაზე დაბრუნება
            self.copy_btn.setText("Copy")

    # მეთოდი, რომელიც გადასცემს ბარათის ინფორმაციას მთავარ გვერდს "Edit"-ზე დაჭერისას
    def edit_clicked(self):
        # მთავარი კლასის open_edit_mode მეთოდის გამოძახება და ყველა შენახული ველის მიწოდება
        self.main_app.open_edit_mode(
            self.password_id, self.title, self.username, self.password, self.url, self.category
        )