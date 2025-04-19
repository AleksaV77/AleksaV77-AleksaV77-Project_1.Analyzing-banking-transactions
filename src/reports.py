import logging
from functools import wraps
from datetime import datetime, timedelta
from settings import EXCEL_PATH, REPORTS_PATH
from typing import Optional, Dict
from functools import wraps

import pandas as pd
from pandas import date_range

from src.views import open_file

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename="..//logs//app.log",
    encoding="utf-8",
    filemode="w",
)

file_excel = "C:/Users/asurk/PycharmProjects/pythonProject6/data/operations.xlsx"

p = pd.DataFrame({
                'Дата платежа': ['03.01.2018', '05.01.2018', '01.02.2018', '10.03.2018'],
                'Категория': ['Супермаркеты', 'Еда', 'Переводы', 'Супермаркеты'],
                'Сумма операции с округлением': [4068.2, 316.8, 5977.1, 3068.2]})

def decorator_record_file(file_name):
    """Декоратор, который записывает результат выполнения функции в JSON файл."""
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            df = func(*args, **kwargs)
            logger.info('Проверка: являются ли данные датафреймом')
            if isinstance(df, pd.DataFrame):
                logger.info('Запись отчёта в файл')
                df.to_json(file_name, orient="records", lines=True, force_ascii=False)
            else:
                logger.error('Данные не являются датафреймом. В файл записаны не будут')
            return df
        return inner
    return wrapper

@decorator_record_file(REPORTS_PATH)
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> Dict[str, float]:
    """Функция, который считает траты по заданной категории за последние три месяца."""

    try:
        if not date:
            stop_date = datetime.now()
        else:
            stop_date = datetime.strptime(date, "%d.%m.%Y")

        logger.info('Определение даты, для подсчета трат по категориям')
        start_date = stop_date - timedelta(days=90)

        transactions["Дата платежа"] = pd.to_datetime(
                        transactions["Дата платежа"], format="%d.%m.%Y")
        df = transactions[
            (transactions["Дата платежа"] >= start_date) &
            (transactions["Дата платежа"] <= stop_date) &
            (transactions["Категория"] == category)
            ]

        cost_analysis = df["Сумма операции с округлением"].sum()
        res = pd.DataFrame(
            {"Категория": [category],
             "Сумма трат": [cost_analysis]})

        logger.info('Поиск дат и подсчет суммы')
        logger.info(f"Создан отчет для категории '{category}': {cost_analysis}")

    except ValueError as ve:
        logger.error(f"Ошибка значения: {ve}")
        return pd.DataFrame()

    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        return pd.DataFrame()

    return res

if __name__ == "__main__":
    file = open_file(file_excel)
    result = spending_by_category(p, "Топливо", "10.03.2018")
    print(result)
