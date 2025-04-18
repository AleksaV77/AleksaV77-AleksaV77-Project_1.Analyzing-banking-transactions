from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import open_file

@patch("src.utils.pd.read_excel")
def test_open_file_excel(mock_file):
    """Тест чтения существующего файла"""
    df = [{"id": 650703.0}]
    value = pd.DataFrame(df)
    mock_file.return_value = value
    result = "C:/Users/asurk/PycharmProjects/pythonProject5/data/operations.xlsx"

    assert open_file(result) == df


@patch("src.utils.open_file")
def test_open_file_excel_2(mock_file):
    """Тестирование чтения при отсутствии файла"""
    df = []
    value = pd.DataFrame(df)
    mock_file.return_value = value
    result = "C:/Users/asurk/PycharmProjects/Homework_Project1/data/operations.xlsx"
    assert open_file(result) == f"файл {result} не найден"


@patch("src.utils.open_file")
def test_open_file_not_excel(mock_file):
    """Тестирование чтения пустого файла"""
    df = []
    value = pd.DataFrame(df)
    mock_file.return_value = value
    assert open_file([]) == []
