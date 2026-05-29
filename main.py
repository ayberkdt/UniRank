import sys
import logging
import traceback
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from unirank.ui.main_window import MainWindow
from unirank.ui.theme import ThemeConfig, apply_theme
from unirank.utils.helpers import LOG_PATH

def setup_logging():
    from logging.handlers import RotatingFileHandler
    
    # 5 MB log file, max 3 backups
    handler = RotatingFileHandler(LOG_PATH, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

def main() -> None:
    setup_logging()
    logging.info("=== UniRank Starting ===")

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
