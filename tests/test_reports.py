import pytest
import pandas as pd

from src.reports import spending_by_category

@pytest.mark.parametrize(
    "df, category",
[
        (pd.DataFrame({
                'dat': ['03.01.2018', '05.01.2018', '01.02.2018', '10.03.2018'],
                'category': ['Супермаркеты', 'Еда', 'Переводы', 'Супермаркеты'],
                'amount': [4068.2, 316.8, 5977.1, 3068.2]
            }),
            pd.DataFrame({
                "Категория": ['Переводы'],
                "Сумма трат": [5977.1]}))]
)

def test_by_category(df, category):
    """Тест на траты по заданной категории за последние три месяца"""
    result = spending_by_category(df, 'Переводы', '01.02.2018')
    # pd.testing.assert_frame_equal(result, category)
    assert result == category
