import json
import logging
from typing import Any

import pandas as pd
import openpyxl

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename="..//logs//app.log",
    encoding="utf-8",
    filemode="w",
)

file_excel = "C:/Users/asurk/PycharmProjects/pythonProject6/data/operations.xlsx"


def open_file(file_name):
    """Функция, которая получает данные из файла"""

    logger.info('Чтение данных из exel-файла')
    try:
        df = pd.read_excel(file_name)
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return f"файл {file_name} не найден"
    except Exception:
        return []


def write_xlsx(file_path: str) -> tuple[list[dict], pd.DataFrame]:
    """ Открытие и запись json данных"""
    try:
        logger.info("Чтение данных из Excel-файла")

        df = pd.read_excel(file_path)

        logger.info("Проверка данных из файла на корректность")

        if isinstance(df, pd.DataFrame) and not df.empty:
            logger.info("Данные корректны. Конвертация в словарь и возврат DataFrame")
            return df.to_dict(orient="records"), df
        else:
            logger.warning("Данные в файле отсутствуют или не являются DataFrame")
            return [], pd.DataFrame()

    except FileNotFoundError:
        logger.warning("Файл по переданному пути отсутствует")
        return [], pd.DataFrame()


def read_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    file = open_file(file_excel)
    l = write_xlsx(file_excel)
    print(l)
