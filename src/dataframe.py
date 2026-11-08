import logging

import pandas as pd

logger = logging.getLogger(__name__)


def df_transactions_csv(file_path: str = "../data_df/transactions.csv") -> list[dict]:
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Успешно прочитан CSV: {file_path}. Строк: {len(data)}")
        return data.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {e}")
        return []


def df_transactions_xlsx(file_path: str = "../data_df/transactions_excel.xlsx") -> list[dict]:
    try:
        data = pd.read_excel(file_path)
        logger.info(f"Успешно прочитан excel: {file_path}. Строк: {len(data)}")
        return data.to_dict(orient="records")
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении excel: {e}")
        return []
