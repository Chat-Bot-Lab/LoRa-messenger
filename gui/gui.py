import getpass
import json
import logging
import sys
from json import JSONDecodeError

from PyQt6 import uic
from PyQt6.QtCore import QIODevice, QTimer
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QMainWindow

from utils.encryption import encrypt, decrypt

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
        self.message_puzzle = ''  # Временное сообщение. Когда сообщение приходит не полностью, собираем по частям.

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
            return
        else:
            data = self.serial.readLine()

            if data:
                try:
                    str_data = data.data().decode().strip()
                    json_data = json.loads(str_data)
                    username = json_data["username"]
                    message = json_data["message"]
                    decrypted_message = decrypt(message)
                    log.info("Username: %s, Message: %s", username, message)
                    self.ui.messageListWidget.addItem(f"{username}: {decrypted_message}")

                except UnicodeDecodeError as e:
                    log.error("Ошибка кодировки: %s", e)

                except JSONDecodeError as e:
                    log.warning("%s. Message is not a json type.", e)

                    if str_data.startswith("{"):   # noqa
                        self.message_puzzle = ''
                        self.message_puzzle += str_data
                        log.warning("Пришло обрывочное сообщение << %s >>", str_data)

                    elif self.message_puzzle and not str_data.endswith("}"):
                        self.message_puzzle += str_data
                        log.warning("Пришло обрывочное сообщение << %s >>", str_data)

                    elif self.message_puzzle and str_data.endswith("}"):
                        log.warning("Пришла последняя часть обрывочного сообщения << %s >>", str_data)
                        self.message_puzzle += str_data

                        json_data = json.loads(self.message_puzzle)
                        self.message_puzzle = ""  # Стираем временное сообщение.
                        username = json_data["username"]
                        message = json_data["message"]
                        decrypted_message = decrypt(message)
                        log.warning("Username: %s, Message: %s", username, decrypted_message)
                        self.ui.messageListWidget.addItem(f"{username}: {message}")

                    else:
                        log.info("incoming message %s", str_data)
                        self.ui.messageListWidget.addItem(str_data)
            else:
                ...

    def sendMessage(self):
        """Отправить сообщение"""

        if not self.serial.isOpen():
            log.warning("Порт не открыт. Соединение не установлено.")
            return

        message = self.ui.messageInputField.text()
        try:
            encrypted_message = encrypt(message)
            self.serial.write(encrypted_message.encode())
            log.info("Сообщение <<< %s >>> отправлено", message)
            self.ui.messageInputField.clear()
        except Exception as e:
            log.info(e)
