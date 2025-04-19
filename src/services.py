import logging
from datetime import datetime

import pandas as pd

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
file = open_file(file_excel)

def cashback_analysis(files, year, month):
    """Функция, которая определяет выгодные категории повышенного кешбэка"""

    list_group = []
    json_analysis = []
    logger.info('Анализ выгодных категорий за месяц')
    for i in files:
        dat = datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S")
        dat_year = dat.strftime("%Y")
        dat_month = dat.strftime("%m")
        category = i["Категория"]
        cash_back = i["Сумма операции с округлением"] * 0.01
        if year == dat_year and month == dat_month:
            list_group.append({'category': category, 'cash_back': cash_back})
            df = pd.DataFrame(list_group)
            df = df.groupby('category', as_index=True).sum().sort_values(by='cash_back', ascending=False).head(3)
            df = df.groupby('category')['cash_back'].head(3)

            json_analysis = df.to_json(orient ='index', force_ascii=False)

    logger.info('Перевод результата к формату json')
    return json_analysis


if __name__ == "__main__":
    file = open_file(file_excel)
    result_json = cashback_analysis(file, '2018', '02')
    print(result_json)