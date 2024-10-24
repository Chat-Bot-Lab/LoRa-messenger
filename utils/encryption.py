from environs import Env

env = Env()
env.read_env()

symbols = env("SYMBOLS")
offset_value = env("OFFSET_VALUE")


def encrypt(message: str) -> str:
    """
    Шифрует сообщение, сдвигая каждый символ в сообщении на заданное значение смещения.
    """
    encr_message = ""
    for symb in message:
        index = symbols.find(symb)
        new_index = index + int(offset_value)
        if new_index > len(symbols) - 1:
            new_index = new_index - (len(symbols) - 1)
        if symb in symbols:
            encr_message += symbols[new_index]
        else:
            encr_message += symb
    return encr_message


def decrypt(message: str) -> str:
    """
    Расшифровывает сообщение, которое ранее было зашифровано с помощью функции encrypt().
    """
    decr_message = ""
    for symb in message:
        index = symbols.find(symb)
        new_index = index - int(offset_value)
        if new_index  < 0:
            new_index  -= 1
        if symb in symbols:
            decr_message += symbols[new_index ]
        else:
            decr_message += symb
    return decr_message
