import sys
import  traceback
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow
from create_password_loginwindow import LoginWindow as Create_Window
from enter_password_loginwindow import LoginWindow as Enter_Window
from verification.verification import is_vault_initialized
from verification.init_db import InitDB
from Front_end.mainpage import Main_Window

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Vault Guard')

class AppController:
    def __init__(self):
        self.auth_window = None
        self.main_window = None
        self.manager = is_vault_initialized()

        # ვამოწმებთ, არის თუ არა ინიციალიზებული
        if not self.manager:
            # ვქმნით რეგისტრაციის ობიექტს (არა კლასს!)
            self.auth_window = Create_Window()
            # ვუკავშირებთ ჩვენს წარმატების სიგნალს გახსნის ფუნქციას
            self.auth_window.success_signal.connect(self.dashboard)
            self.auth_window.show()
        else:
            # ვქმნით შესვლის ობიექტს
            self.auth_window = Enter_Window()
            # თუ შესვლის ფანჯარასაც აქვს ანალოგიური სიგნალი წარმატებულ ავტორიზაციაზე:
            self.auth_window.success_signal.connect(self.dashboard)
            self.auth_window.show()

    def dashboard(self):
        if self.auth_window:
            self.auth_window.close()
        try:
            self.main_window = Main_Window()
            self.main_window.show()
        except Exception:
            import traceback
            traceback.print_exc()

def excepthook(exc_type, exc_value, exc_tb):
    traceback.print_exception(exc_type, exc_value, exc_tb)
    # don't call the default hook, which would abort silently

sys.excepthook = excepthook

def main():
    InitDB()

    app = QApplication(sys.argv)

    controller = AppController()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


