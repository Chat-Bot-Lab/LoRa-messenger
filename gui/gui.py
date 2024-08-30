import getpass
import logging
import sys

from PyQt6 import uic
from PyQt6.QtCore import QIODevice, QTimer
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QMainWindow

log = logging.getLogger(__name__)


class LoRaMessenger(QMainWindow):

    def __init__(self):
        super().__init__()
        self.receivedMessages = None
        self.serial = QSerialPort()
        self.serial.setBaudRate(9600)
        self.port_list = self.get_available_ports()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readSerial)
        self.timer.start(100)

    def initUI(self):
        """Инициализация пользовательского интерфейса."""
        self.ui = uic.loadUi("gui/design.ui", self)
        self.setWindowTitle(f"LoRa Messenger - {getpass.getuser()} - {sys.argv[0].split('/')[-1]}")
        self.ui.portList.addItems(self.port_list)
        self.ui.connectPortButton.clicked.connect(self.connectSerialPort)
        self.ui.disconnectPortButton.clicked.connect(self.disConnectSerialPort)
        self.ui.sendButton.clicked.connect(self.sendMessage)

    @staticmethod
    def get_available_ports():
        """Получить список доступных портов."""
        port_list = []
        ports = QSerialPortInfo().availablePorts()
        if ports:
            for port in ports:
                port_list.append(port.portName())
        else:
            log.warning("Порты не найдены")
        return port_list

    def connectSerialPort(self):
        """Подключить к выбранному порту."""
        log.info("Подключение к порту")
        try:
            self.serial.setPortName(self.ui.portList.currentText())
            self.serial.open(QIODevice.OpenModeFlag.ReadWrite)
            log.info("Подключен к порту %s", self.ui.portList.currentText())
        except Exception as e:
            log.exception("Ошибка подключения: %s", e)

    def disConnectSerialPort(self):
        """Разорвать соединение с портом."""
        self.serial.close()
        log.info("Соединение с портом разорвано.")

    def readSerial(self):
        """Прочитать данные с порта."""
        if not self.serial.isOpen():
            pass
        else:
            data = self.serial.readLine()
            if data:
                str_data = data.data().decode().strip()

                self.ui.messageListWidget.addItem(str_data)
            else:
                pass

    def sendMessage(self):
        """Отправить сообщение"""
        message = self.ui.messageInputField.text()
        if not self.serial.isOpen():
            log.warning("Порт не открыт. Соединение не установлено.")
            return
        try:
            self.serial.write(message.encode())
            log.info("Сообщение <<< %s >>> отправлено", message)
            self.ui.messageInputField.clear()
        except Exception as e:
            log.info(e)
