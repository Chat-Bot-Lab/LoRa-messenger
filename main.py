import logging
import sys

from PyQt6 import QtWidgets

from config.configure_logger import configure_logging
from gui.gui import LoRaMessenger

if __name__ == "__main__":
    configure_logging(logging.INFO)
    app = QtWidgets.QApplication([])
    messanger = LoRaMessenger()
    messanger.show()
    sys.exit(app.exec())