import logging
import re
from datetime import datetime, time, timedelta

from src.utils import open_file

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(filename)s: %(levelname)s: %(message)s",
    filename="..//logs//app.log",
    encoding="utf-8",
    filemode="w",
)

file_excel = "C:/Users/asurk/PycharmProjects/pythonProject6/data/operations.xlsx"
result_file = {}

def greeting_user(hour):
    """Функция, которая приветствует пользователя"""

    str_date = datetime.strptime(hour, "%H:%M:%S")
    night = time(0, 6)
    morning = time(6, 12)
    day = time(12, 17)
    evening = time(17, 0)

    logger.info('Определение времени суток для приветствия')

    if night <= str_date.time() < morning:
        result_file["greeting"] = "Доброй ночи"
    elif morning <= str_date.time() < day:
        result_file["greeting"] = "Доброе утро"
    elif day <= str_date.time() < evening:
        result_file["greeting"] = "Добрый день"
    else:
        result_file["greeting"] = "Добрый вечер"

    logger.info("Приветствие готово")
    return result_file


def search_date(files, input_date):
    """Функция, возвращающая список, отфильтрованный по дате с начала месяца, на который выпадает входящая дата,
    по входящую дату."""

    pattern = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")

    result_file = []
    logger.info('Проверка формата даты')
    if input_date and pattern.fullmatch(input_date):

        day_int = int(input_date[:2])

        input_date_obj = datetime.strptime(input_date, "%d.%m.%Y").date()

        start = input_date_obj - timedelta(days=(day_int - 1))
        stop = input_date_obj
        logger.info('Фильтрация операций по дате')
        for i in files:
            operation_date_obj = datetime.strptime(i["Дата операции"], "%d.%m.%Y %H:%M:%S").date()

            if start <= operation_date_obj <= stop:
                result_file.append(i)
    else:
        print("Введена неверная дата. Введите дату в формате ДД.ММ.ГГГГ")
        logger.info('Не верный формат даты')

    return result_file


def card_user_info(files):
    """Функция, которая определяет номер карты по последним 4 цифрам"""

    result_file["cards"] = []
    logger.info('Определение номеров карт')
    try:
        logger.info('Подсчёт суммы и кэшбека по картам')
        for card in files:
            amount = str(card["Сумма платежа"])[1:]
            if isinstance(card["Номер карты"], str):
                last_card = card.get("Номер карты")[1:]
                if not any(card["last_digits"] == last_card for card in result_file["cards"]):
                    result_file["cards"].append({"last_digits": last_card,
                                                "total_spent": 0,
                                                 "cashback": 0})
                for i in result_file["cards"]:
                    if i["last_digits"] == last_card:
                        if "-" in str(card["Сумма платежа"]):
                            cash_back = float(amount) / 100
                        else:
                            continue
                        i["total_spent"] += float(amount)
                        i["cashback"] += cash_back
        logger.info('Результат с данных по катам готов')
        return result_file["cards"]
    except Exception as es:
        return es

def top_transaction(files):
    """Функция, которая показывает топ 5 транзаций по сумме платежа"""

    result_file["top_transactions"] = []
    logger.info('Подсчёт суммы по категориям')
    for i in files:
        dat = i.get("Дата операции")
        amount = i["Сумма операции с округлением"]
        category = i.get("Категория")
        description = i.get("Описание")
        val = i.get("Валюта платежа")
        if not any(i["category"] == category for i in result_file["top_transactions"]):
            result_file["top_transactions"].append({"date": dat, "amount": 0,
                                         "category": category, "description": description, "v": val})
        for top in result_file["top_transactions"]:
            if top["category"] == category:
                if amount >= top["amount"]:
                    top["amount"] = amount
        sort_sum = sorted(result_file["top_transactions"], key=lambda x: x["amount"], reverse=True)
        result_file["top_transactions"] = sort_sum[:5]
    logger.info('Определены топ 5 транзаций по сумме платежа')

    return result_file["top_transactions"]


if __name__ == "__main__":
    file = open_file(file_excel)
    result_file = greeting_user("08:30:00")
    filter_file = search_date(file, "06.01.2018")
    result = card_user_info(filter_file)
    result_file = top_transaction(filter_file)
    print(result_file)
