import pytest
import pandas as pd

from src.reports import spending_by_category

@pytest.mark.parametrize(
    "df, category",
[
        (pd.DataFrame({
                'Дата платежа': ['03.01.2018', '05.01.2018', '01.02.2018', '10.03.2018'],
                'Категория': ['Супермаркеты', 'Еда', 'Переводы', 'Супермаркеты'],
                'Сумма операции с округлением': [4068.2, 316.8, 5977.1, 3068.2]
            }),
            pd.DataFrame({
                "Категория": ['Переводы'],
                "Сумма трат": [5977.1]}))]
)

def test_by_category(df, category):
    """Тест на траты по заданной категории за последние три месяца"""
    result = spending_by_category(df, 'Переводы', '01.02.2018')
    pd.testing.assert_frame_equal(result, category)

@pytest.mark.parametrize(
    "df, category",
[
        (pd.DataFrame({
                'Дата платежа': ['07.03.2018', '05.03.2018', '01.04.2018', '15.05.2018'],
                'Категория': ['Топливо', 'Еда', 'Топливо', 'Супермаркеты'],
                'Сумма операции с округлением': [4000.2, 500.8, 1500.1, 700.2]
            }),
            pd.DataFrame({
                "Категория": ['Топливо'],
                "Сумма трат": [5500.3]}))]
)

def test_by_category_not(df, category):
    """Тест на траты по заданной категории за последние три месяца"""
    result = spending_by_category(df, 'Топливо', '01.04.2018')
    pd.testing.assert_frame_equal(result, category)
