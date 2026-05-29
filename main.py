import sys
import logging
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from unirank.ui.main_window import MainWindow
from unirank.ui.main_window import MainWindow
from unirank.ui.theme import ThemeConfig, apply_theme

def main() -> None:

    # High-DPI: Qt6 genelde otomatik, ama gerekirse burada kontrol edebilirsin.
    app = QApplication(sys.argv)

    # Theme
    cfg = ThemeConfig()
    # Strict: tema uygulanamazsa uygulama başlatma (sessiz fallback yok)
    apply_theme(app, cfg)

    # Main window
    w = MainWindow(theme=cfg)
    w.show()
    logging.info("MainWindow shown")
    # Run
    try:
        sys.exit(app.exec())
    except Exception:
        logging.exception("Fatal error in Qt event loop")
        raise


if __name__ == "__main__":
    main()
if __name__ == '__main__':
    main()
