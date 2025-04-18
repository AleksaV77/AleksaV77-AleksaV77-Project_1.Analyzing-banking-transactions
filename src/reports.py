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

    list_group = []
    res = []

    if not date:
        stop_date = datetime.now()
    else:
        stop_date = datetime.strptime(date, "%d.%m.%Y")

    logger.info('Определение даты, для подсчета трат по категориям')
    start_date = stop_date - timedelta(days=90)

    for i in transactions:
        i["Дата платежа"] = pd.to_datetime(
                    i["Дата платежа"], format="%d.%m.%Y")
        if category == i["Категория"]:
            list_group.append({
                'dat': i["Дата платежа"], 'category': category, 'amount': i["Сумма операции с округлением"]})
            df = pd.DataFrame(list_group)
            df = df.loc[(df['dat'] >= start_date) & (df['dat'] <= stop_date)]
            cost_analysis = df["amount"].abs().sum()
            res = pd.DataFrame(
                {"Категория": [category],
                 "Сумма трат": [cost_analysis]})

            logger.info('Поиск дат и подсчет суммы')
            logger.info(f"Создан отчет для категории '{category}': {cost_analysis}")
    return res

if __name__ == "__main__":
    file = open_file(file_excel)
    result = spending_by_category(file, "Переводы", "04.09.2021")
    print(result)
