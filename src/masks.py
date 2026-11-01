import logging
from pathlib import Path


# Создаем папку logs
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Настраиваем логгер модуля
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создаем хендлер для файла
file_handler = logging.FileHandler(LOG_DIR / 'masks.log', mode="w", encoding="utf-8")

# Создаем форматер для файла
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Добавляем хендлер к логгеру
logger.addHandler(file_handler)

"""Функция
get_mask_card_number
 принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован и отображается в формате
XXXX XX** **** XXXX, где X — это цифра номера. То есть видны первые 6 цифр и последние 4 цифры,
остальные символы отображаются звездочками, номер разбит по блокам по 4 цифры, разделенным пробелами.
Пример работы функции:
7000792289606361     # входной аргумент
7000 79** **** 6361  # выход функции"""


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки банковской карты
    При введении неверных данных будет вызывать ValueError"""

    if not card_number:
        logger.error("Номер карты не может быть пустым. Ошибка: ValueError")
        raise ValueError("Номер карты не может быть пустым!")
    if not card_number.isdigit():
        logger.error("Номер карты должен содержать только цифры!. Ошибка ValueError")
        raise ValueError("Номер карты должен содержать только цифры!")
    if len(card_number) != 16:
        logger.error("Номер карты должен содержать 16 символов. Ошибка ValueError")
        raise ValueError("Номер карты должен содержать 16 символов")
    result = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    logger.info(f"Код выполнен. Результат: {result}")
    return result


""" Функция
get_mask_account
принимает на вход номер счета и возвращает его маску. Номер счета замаскирован и отображается в формате
**XXXX, где X — это цифра номера. То есть видны только последние 4 цифры номера, а перед ними — две звездочки.
Пример работы функции:
73654108430135874305  # входной аргумент
**4305  # выход функции """


def get_mask_account(number_account: str) -> str:
    """Функция маскировки номера банковского счета

    При введении неверных данных будет вызывать ValueError"""
    if not number_account:
        logger.error("Номер счета не должен быть пустым. Ошибка: ValueError")
        raise ValueError("Номер счета не должен быть пустым!")
    if not number_account.isdigit():
        logger.error("Номер счета должен содержать только цифры!. Ошибка: ValueError")
        raise ValueError("Номер счета должен содержать только цифры!")
    if len(number_account) >= 4:
        result = f"**{number_account[-4:]}"
        logger.info(f"Код выполнен. Результат: {result}")
        return result
    logger.error("Номер счета должен содержать больше 4 символов. Ошибка: ValueError")
    raise ValueError("Номер счета должен содержать больше 4 символов")
