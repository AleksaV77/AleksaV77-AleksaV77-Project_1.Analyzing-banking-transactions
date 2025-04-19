from datetime import datetime

import pandas as pd

from src.utils import open_file, write_xlsx
from settings import EXCEL_PATH
from src.views import greeting_user, search_date, card_user_info, top_transaction, result_file
from src.services import cashback_analysis
from src.reports import spending_by_category

file_excel = "C:/Users/asurk/PycharmProjects/pythonProject5/data/operations.xlsx"

def main():
    """Функция для запуска всего проекта"""

    # Открываем файл
    file = open_file(file_excel)

    # Приветствие
    greeting_user("18:55:21")

    # Фильтр с начала месяца по дату
    filter_file = search_date(file, "30.07.2021")

    # Определение номера карт
    card_user_info(filter_file)

    # Топ-5
    top_transaction(filter_file)

    # Выгодный кешбек
    cashback = cashback_analysis(file, '2021', '09')

    # Траты за 3 месяца
    by_category = spending_by_category(df, "Переводы", "10.03.2018")

    return (f"Страница «Главная»\n{result_file}\n"
            f"\nВыгодные категории повышенного кешбэка за месяц:\n{cashback}\n"
            f"\nТраты по заданной категории за последние три месяца:\n{by_category}\n")


if __name__ == "__main__":
    operations_list, df = write_xlsx(file_excel)
    print(main())

