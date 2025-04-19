import pytest

from src.services import cashback_analysis

def test_cashback_analysis(operations_list, test_result_cashback):
    """Тест на определение выгодных категорий повышенного кешбэка"""
    assert cashback_analysis(operations_list, '2018', '02') == test_result_cashback

def test_cashback_analysis_2(operations_list, test_result_cashback):
    """Тест на определение выгодных категорий повышенного кешбэка"""
    assert cashback_analysis(operations_list, '2019', '02') == []

def test_cashback_analysis_3(operations_list, test_result_cashback):
    """Тест на определение выгодных категорий повышенного кешбэка"""
    assert cashback_analysis(operations_list, '2021', '02') == []
