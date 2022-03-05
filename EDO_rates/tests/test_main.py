from multiprocessing.sharedctypes import Value
import pytest
from EDO_rates.main import *
import datetime

def test_get_edo_rate():
    assert get_edo_rate('1231') == 1.7

def test_get_user_dates(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: ['12-21', '01-15'])

    date1 = datetime.datetime.strptime('12-21','%m-%y')
    date2 = datetime.datetime.strptime('01-15','%m-%y')

    assert date1, date2 == ['12-21', '01-15']

validate_input_data_test_array = [
    ('q', [None, True]),
    ('a', [None, False]),
    ('01-21', [datetime.datetime.strptime('01-21','%m-%y'), False]),
]
@pytest.mark.parametrize('sample, expected', validate_input_data_test_array)
def test_validate_input_data(sample, expected):
    date_user, end = validate_input_data(sample)

    assert [date_user, end] == expected
