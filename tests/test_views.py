from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.views import greeting_user, search_date, card_user_info, top_transaction


@pytest.mark.parametrize(
    "input_time, expected_greet",
    [
        ("08:30:00", {'greeting': "Доброе утро"}),
        ("15:30:00", {'greeting': "Добрый день"}),
        ("23:59:59", {'greeting': "Добрый вечер"}),
        ("04:30:03", {'greeting': "Доброй ночи"}),
    ],
)

def test_greetings(input_time, expected_greet):
    """Тест, приветствие пользователя"""
    result = greeting_user(input_time)

    assert result == expected_greet


def test_search_date(operations_list, list_search_date):
    """Тест, фильтровации по дате с начала месяца"""

    assert search_date(operations_list, "06.01.2018") == list_search_date

def test_card_user_info(operations_list, test_result_card_user):
    """Тест, определения номера карты по последним 4 цифрам"""
    assert card_user_info(operations_list) == test_result_card_user


def test_top_transaction(operations_list, test_result_top_trans):
    """Тест, топ 5 транзаций по сумме платежа"""
    assert top_transaction(operations_list) == test_result_top_trans
