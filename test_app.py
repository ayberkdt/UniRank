import sys
import traceback

def my_excepthook(type, value, tback):
    print("GLOBAL EXCEPTHOOK CAUGHT ERROR:", file=sys.stderr)
    traceback.print_exception(type, value, tback)
    sys.__excepthook__(type, value, tback)

sys.excepthook = my_excepthook

from PyQt6.QtWidgets import QApplication
from unirank.ui.theme import ThemeConfig, apply_theme
from unirank.ui.main_window import MainWindow

app = QApplication(sys.argv)
cfg = ThemeConfig()
apply_theme(app, cfg)
w = MainWindow(theme=cfg)
w.show()
sys.exit(app.exec())
