from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
from qfluentwidgets import (FluentWindow, Theme, FluentIcon as FIF, setTheme)
from dashboard import DashBoardPage
from password_page import PasswordPage
from file_page import FilePage
from report_page import ThreatAnalysisPage
from quarantine_page import QuarantinePage

class Main_Window(FluentWindow):
    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setWindowTitle("Vault Guard")
        self.setWindowIcon(QIcon('vaulticon.webp'))
        self.setWindowFlags(Qt.Window)
        self.resize(1280, 720)
        self.showMaximized()

        self.dashboardpage = DashBoardPage()
        """ იმისათვის რომ ფანჯრებმა ილაპარაკონ საჭიროა მათი ერთმანეთტანდაკავშირება,
        ამიტომაც ყოველ ფანჯარას მივეცი self რათა დაიმახსოვროს მთავარი გვერდი და მასტან კავშირი ჰქონდეს"""
        self.passwordpage = PasswordPage(self)
        self.filepage = FilePage(self)
        self.threatanalysispage = ThreatAnalysisPage(self)
        self.quarantinepage = QuarantinePage(self)

        self.addSubInterface(
            self.dashboardpage,
            FIF.HOME,
            'Dashboard'
        )
        self.addSubInterface(
            self.passwordpage,
            FIF.HIDE,
            'პაროლი'
        )
        self.addSubInterface(
            self.filepage,
            FIF.FOLDER,
            'ფაილები'
        )
        self.addSubInterface(
            self.threatanalysispage,
            FIF.FINGERPRINT,
            'საფრთხის ანალიტიკა'
        )
        self.addSubInterface(
            self.quarantinepage,
            FIF.FILTER,
            'Quarantine'
        )



