import sys
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QApplication

# QFluentWidgets ბიბლიოთეკის კომპონენტები მომხმარებლის ინტერფეისისთვის
from qfluentwidgets import (
    CardWidget, SubtitleLabel, CaptionLabel,
    LargeTitleLabel, FluentIcon, IconWidget, SmoothScrollArea,
    setTheme, Theme
)

# Matplotlib-ის ინტეგრაცია PyQt5-თან ვიზუალური გრაფიკების ასაგებად
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Matplotlib-ის გლობალური კონფიგურაცია მუქი თემისთვის (Dark Theme)
# ეს უზრუნველყოფს, რომ გრაფიკები იდეალურად ჩაჯდეს QFluentWidgets-ის დიზაინში
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#1c1c1c'  # მთავარი ფანჯრის ფონის ფერი
plt.rcParams['axes.facecolor'] = '#202020'  # უშუალოდ გრაფიკის სამუშაო არეს ფონი
plt.rcParams['font.size'] = 9  # ტექსტის ზომა გრაფიკებზე
plt.rcParams['text.color'] = '#ffffff'  # ძირითადი ტექსტის ფერი
plt.rcParams['axes.labelcolor'] = '#aaaaaa'  # ღერძების დასახელებების ფერი
plt.rcParams['xtick.color'] = '#888888'  # X ღერძის დანაყოფების ფერი
plt.rcParams['ytick.color'] = '#888888'  # Y ღერძის დანაყოფების ფერი


class AnalyticsChartCanvas(FigureCanvas):
    """
    კლასი უზრუნველყოფს Matplotlib-ის გრაფიკის გარდაქმნას Qt კომპონენტად (Widget).
    მიმდინარეობს მინიმალური სიმაღლის განსაზღვრა, რათა გრაფიკები არ შეიკუმშოს.
    """

    def __init__(self, fig):
        super().__init__(fig)
        self.setMinimumHeight(280)


class KPICard(CardWidget):
    """
    სტატისტიკური ბარათის (KPI Card) კლასი, მორგებული Fluent Dark დიზაინზე.
    გამოიყენება ისეთი ინფორმაციისთვის, როგორიცაა პაროლების რაოდენობა, საფრთხეები და ა.შ.
    """

    def __init__(self, title: str, value: str, icon: FluentIcon, is_alert=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(185, 90)  # ბარათის ფიქსირებული ზომები

        # ბარათის ვიზუალური სტილი: ფონი, კანტები და მომრგვალება
        self.setStyleSheet("""
            KPICard {
                background-color: #202020;
                border: 1px solid #2d2d2d;
                border-radius: 8px;
            }
        """)

        # მთავარი ჰორიზონტალური განლაგება (ხატულა მარცხნივ, ტექსტები მარჯვნივ)
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # ფანჯრის ხატულის (Icon) შექმნა და ზომის გაწერა
        self.icon_widget = IconWidget(icon)
        self.icon_widget.setFixedSize(28, 28)

        # თუ ბარათი არის საგანგაშო (მაგალითად, ნაპოვნია საფრთხე), ხატულა ხდება წითელი
        if is_alert and value != "0":
            self.icon_widget.setStyleSheet("color: #ff4d4d;")
        else:
            self.icon_widget.setStyleSheet("color: #60cdff;")  # სტანდარტულად ლურჯი

        main_layout.addWidget(self.icon_widget, alignment=Qt.AlignVCenter)

        # ტექსტების ვერტიკალური განლაგება (სათაური ზემოთ, მნიშვნელობა ქვემოთ)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        self.title_label = CaptionLabel(title)
        self.title_label.setStyleSheet("color: #b0b0b0;")  # ნაცრისფერი სათაური
        self.value_label = SubtitleLabel(value)
        self.value_label.setStyleSheet("color: #ffffff; font-weight: bold;")  # თეთრი, გამსხვილებული ციფრი

        # საგანგაშო ბარათის შემთხვევაში ციფრიც წითლდება
        if is_alert and value != "0":
            self.value_label.setStyleSheet("color: #ff4d4d; font-weight: bold;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.value_label)

        # კომპონენტების საბოლოო აწყობა ბარათის შიგნით
        main_layout.addLayout(text_layout)
        main_layout.addStretch()  # დარჩენილი თავისუფალი სივრცის შევსება მარჯვნივ


class ThreatAnalysisPage(QWidget):
    """
    საფრთხეების ანალიტიკის მთავარი გვერდი.
    იღებს main_window-ის რეფერენსს ნავიგაციის ან გლობალური მართვისთვის.
    """

    def __init__(self, main_window):
        super().__init__()
        # ობიექტის და ფანჯრის იდენტიფიკატორები
        self.setObjectName("საფრთხის ანალიტიკა")
        self.setWindowTitle("ThreatAnalysis Page")
        self.main_window = main_window

        # მომხმარებლის ინტერფეისის (UI) აწყობა
        self.init_ui()

    def init_ui(self):
        # გვერდის ძირითადი Layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # გლუვი სქროლინგის არე (Smooth Scroll Area) დიდი ეკრანების ან პატარა რეზოლუციებისთვის
        self.scroll_area = SmoothScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: #1c1c1c; }")

        # კონტენტის კონტეინერი, რომელიც ჩაჯდება სქროლში
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: #1c1c1c;")
        self.content_layout = QVBoxLayout(self.scroll_content)
        self.content_layout.setContentsMargins(25, 25, 25, 25)

        # გვერდის მთავარი სათაური
        self.title = LargeTitleLabel("Advanced Security Analytics & Vault Report", self)
        self.title.setStyleSheet("color: #ffffff;")
        self.content_layout.addWidget(self.title)
        self.content_layout.addSpacing(15)

        # --- სექცია 1: KPI ბარათების ბადე (6 ანალიტიკური ქარდი) ---
        kpi_grid = QGridLayout()
        kpi_grid.setSpacing(10)

        # ბარათების ინიციალიზაცია შესაბამისი პარამეტრებით, ხატულებითა და სტატუსებით
        self.card_total_pw = KPICard("Total Passwords", "142", FluentIcon.VPN, parent=self)
        self.card_weak_pw = KPICard("Weak Passwords", "8", FluentIcon.INFO, is_alert=True, parent=self)
        self.card_levenshtein = KPICard("Similar (Lev.)", "14", FluentIcon.PEOPLE, parent=self)
        self.card_total_files = KPICard("Total Files", "54", FluentIcon.FOLDER, parent=self)
        self.card_magic_anomalies = KPICard("Type Anomalies", "2", FluentIcon.BOOK_SHELF, is_alert=True, parent=self)
        self.card_rules_triggered = KPICard("Quarantined", "3", FluentIcon.FINGERPRINT, is_alert=True, parent=self)

        # ბარათების განლაგება მატრიცაში (0 რიგი, სვეტები 0-დან 5-მდე)
        kpi_grid.addWidget(self.card_total_pw, 0, 0)
        kpi_grid.addWidget(self.card_weak_pw, 0, 1)
        kpi_grid.addWidget(self.card_levenshtein, 0, 2)
        kpi_grid.addWidget(self.card_total_files, 0, 3)
        kpi_grid.addWidget(self.card_magic_anomalies, 0, 4)
        kpi_grid.addWidget(self.card_rules_triggered, 0, 5)

        self.content_layout.addLayout(kpi_grid)
        self.content_layout.addSpacing(20)

        # --- სექცია 2: დიაგრამების მატრიცა (2x2 Grid) ---
        charts_grid = QGridLayout()
        charts_grid.setSpacing(15)

        # გრაფიკების ჩამოსასხმელი კონტეინერების (CardWidget) სტილი
        card_style = "CardWidget { background-color: #202020; border: 1px solid #2d2d2d; border-radius: 8px; }"

        # 1. პაროლების სიმტკიცე (წრიული დიაგრამა / Pie Chart)
        c1_card = CardWidget(self)
        c1_card.setStyleSheet(card_style)
        c1_layout = QVBoxLayout(c1_card)
        lbl1 = SubtitleLabel("Password Strength Distribution")
        lbl1.setStyleSheet("color: #ffffff;")
        c1_layout.addWidget(lbl1)
        c1_layout.addWidget(self.create_password_pie_chart())  # გრაფიკის ჩამატება
        charts_grid.addWidget(c1_card, 0, 0)

        # 2. საფრთხის ინდექსი (სვეტოვანი დიაგრამა / Bar Chart)
        c2_card = CardWidget(self)
        c2_card.setStyleSheet(card_style)
        c2_layout = QVBoxLayout(c2_card)
        lbl2 = SubtitleLabel("Threat Scoring Engine Metrics")
        lbl2.setStyleSheet("color: #ffffff;")
        c2_layout.addWidget(lbl2)
        c2_layout.addWidget(self.create_threat_bar_chart())  # გრაფიკის ჩამატება
        charts_grid.addWidget(c2_card, 0, 1)

        # 3. შენონის ენტროპია (გაბნევის დიაგრამა / Scatter Plot)
        c3_card = CardWidget(self)
        c3_card.setStyleSheet(card_style)
        c3_layout = QVBoxLayout(c3_card)
        lbl3 = SubtitleLabel("Shannon Entropy vs File Size")
        lbl3.setStyleSheet("color: #ffffff;")
        c3_layout.addWidget(lbl3)
        c3_layout.addWidget(self.create_entropy_scatter_plot())  # გრაფიკის ჩამატება
        charts_grid.addWidget(c3_card, 1, 0)

        # 4. ფაილის მთლიანობა (დონატისებრი დიაგრამა / Donut Chart)
        c4_card = CardWidget(self)
        c4_card.setStyleSheet(card_style)
        c4_layout = QVBoxLayout(c4_card)
        lbl4 = SubtitleLabel("Magic Bytes & SHA-256 Analysis")
        lbl4.setStyleSheet("color: #ffffff;")
        c4_layout.addWidget(lbl4)
        c4_layout.addWidget(self.create_integrity_donut_chart())  # გრაფიკის ჩამატება
        charts_grid.addWidget(c4_card, 1, 1)

        # სტრუქტურის საბოლოო შეკვრა სქროლბართან
        self.content_layout.addLayout(charts_grid)
        self.content_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

    def create_password_pie_chart(self):
        """ ქმნის პაროლების ხარისხობრივი განაწილების წრიულ დიაგრამას """
        labels = ['Very Strong', 'Strong', 'Medium', 'Weak']
        sizes = [45, 30, 15, 10]  # პროცენტული წილები
        colors = ['#107c41', '#2b579a', '#fcd116', '#ff4d4d']  # მწვანე, ლურჯი, ყვითელი, წითელი

        fig, ax = plt.subplots(figsize=(4, 3))
        # wedgeprops განსაზღვრავს შიდა ცარიელ სივრცეს დონატის სტილის მისაღებად
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=120, colors=colors,
               textprops={'fontsize': 8, 'color': 'white'}, wedgeprops=dict(width=0.5, edgecolor='#202020'))
        fig.tight_layout()
        return AnalyticsChartCanvas(fig)

    def create_threat_bar_chart(self):
        """ ქმნის ფაილების საფრთხის დონეების სვეტოვან დიაგრამას """
        categories = ['Low (0-30)', 'Medium (31-70)', 'High (71-100)']
        counts = [39, 12, 3]  # ფაილების რაოდენობა კატეგორიებში
        colors = ['#107c41', '#fcd116', '#ff4d4d']

        fig, ax = plt.subplots(figsize=(4, 3))
        bars = ax.bar(categories, counts, color=colors, width=0.5, edgecolor='#2d2d2d')
        ax.set_ylabel('File Count', fontsize=8, color='#aaaaaa')
        ax.tick_params(colors='#888888', labelsize=8)

        # მნიშვნელობების (ციფრების) დაწერა უშუალოდ სვეტების თავზე
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, yval + 0.3, str(yval), ha='center', va='bottom', weight='bold',
                    fontsize=8, color='white')
        fig.tight_layout()
        return AnalyticsChartCanvas(fig)

    def create_entropy_scatter_plot(self):
        """ აგებს ენტროპიისა და ფაილის ზომის დამოკიდებულების გრაფიკს ანომალიების საპოვნელად """
        fig, ax = plt.subplots(figsize=(4, 3))

        # რანდომული მონაცემების გენერაცია სიმულაციისთვის
        np.random.seed(42)
        sizes_mb = np.random.uniform(0.1, 50, 40)  # ფაილის ზომები
        entropy = np.random.uniform(4.0, 7.3, 40)  # ნორმალური ენტროპია

        # საეჭვო (ძალიან მაღალი ენტროპიის მქონე) ფაილების გენერაცია (მაგ. დაშიფრული/ვირუსი)
        malicious_sizes = np.random.uniform(5, 30, 4)
        malicious_entropy = np.random.uniform(7.6, 7.99, 4)

        # წერტილების დასმა გრაფიკზე (უსაფრთხო - ლურჯი, საეჭვო - წითელი X ნიშნით)
        ax.scatter(sizes_mb, entropy, color='#60cdff', alpha=0.7, label='Safe')
        ax.scatter(malicious_sizes, malicious_entropy, color='#ff4d4d', s=60, marker='X', label='Suspicious (7.5+)')

        # კრიტიკული ზღვარის (7.5 ენტროპია) აღმნიშვნელი ჰორიზონტალური წყვეტილი ხაზი
        ax.axhline(y=7.5, color='#ff4d4d', linestyle='--', linewidth=1, alpha=0.7)

        ax.set_xlabel('File Size (MB)', fontsize=8, color='#aaaaaa')
        ax.set_ylabel('Shannon Entropy', fontsize=8, color='#aaaaaa')
        ax.legend(loc='lower right', fontsize=7, facecolor='#202020', edgecolor='#2d2d2d')
        ax.tick_params(colors='#888888', labelsize=8)
        fig.tight_layout()
        return AnalyticsChartCanvas(fig)

    def create_integrity_donut_chart(self):
        """ ქმნის ფაილების მთლიანობისა და ჰეშების ვალიდურობის დონატისებრ დიაგრამას """
        labels = ['Valid Match', 'SHA-256 Duplicates', 'Magic Byte Mismatch']
        sizes = [85, 11, 4]
        colors = ['#107c41', '#ff8c00', '#ff4d4d']

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
               textprops={'fontsize': 8, 'color': 'white'}, pctdistance=0.75)

        # შუაში თეთრი/მუქი წრის დადება დონატის (Donut) ეფექტის მისაღებად
        centre_circle = plt.Circle((0, 0), 0.55, fc='#202020')
        fig.gca().add_artist(centre_circle)
        fig.tight_layout()
        return AnalyticsChartCanvas(fig)