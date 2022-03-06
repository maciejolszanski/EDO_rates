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

validate_input_data_test_data = [
    ('q', [None, True]),
    ('a', [None, False]),
    ('01-21', [datetime.datetime.strptime('01-21','%m-%y').date(), False]),
]
@pytest.mark.parametrize('sample, expected', validate_input_data_test_data)
def test_validate_input_data(sample, expected):
    date_user, end = validate_input_data(sample)

    assert [date_user, end] == expected

validate_dates_input_data = [
    (datetime.date(2012, 2, 1), datetime.date(2015,8,1), True),
    (datetime.date(2022, 2, 1), datetime.date(2015,8,1), False),
    (datetime.date(2022, 2, 1), datetime.date(2022,2,1), False),
    (datetime.date(2036, 2, 1), datetime.date(2015,8,1), False),
    (datetime.date(2022, 2, 1), datetime.date(2036,8,1), False),
]
@pytest.mark.parametrize('date1, date2, expected', validate_dates_input_data)
def test_validate_dates(date1, date2, expected):
    assert validate_dates(date1, date2) == expected

@pytest.fixture
def dates():
    date1 = datetime.date(2012, 1, 1)
    date2 = datetime.date(2012, 2, 1)
    date3 = datetime.date(2012, 3, 1)

    dates = [date1, date2, date3]

    return dates

def test_get_dates_to_check(dates):
    date1 = datetime.date(2012, 1, 1)
    date2 = datetime.date(2012, 3, 1)

    assert get_dates_to_check(date1, date2) == dates

def test_get_exp_str(dates):
    exp_str = get_exp_str(dates)
    assert exp_str == ['0122', '0222', '0322']