import pytest
from EDO_rates.edo_handler import EdoHandler
import datetime
from unittest import mock

def test_get_edo_rate():
    eh = EdoHandler()
    assert eh.get_edo_rate('1231') == 1.7

def test_get_single_date_valid():
    with mock.patch('builtins.input', return_value="12-21"):
        eh = EdoHandler()
        date1 = datetime.date(2021, 12, 1)
        assert list(eh.get_single_date('initial')) == [date1, False]

def test_get_single_date_not_valid():
    with mock.patch('builtins.input', return_value="21-21"):
        eh = EdoHandler()
        assert list(eh.get_single_date('initial')) == [None, False]

def test_get_single_date_exit():
    with mock.patch('builtins.input', return_value="q"):
        eh = EdoHandler()
        assert list(eh.get_single_date('initial')) == [None, True]

""" I cannot patch multiple methods
def get_fake_get_single_data(date, end):
    '''fake function for testing get_user_dates'''
    return date, end

@mock.patch.object(EdoHandler, 'get_single_date', get_fake_get_single_data(datetime.date(2020, 12, 1), False))
def test_get_user_dates_ok():
    date1 = datetime.date(2020, 12, 1)
    date2 = datetime.date(2021, 12, 1)

    eh = EdoHandler()
    assert list(eh.get_user_dates()) == [date1, date2, False]
"""

validate_input_data_test_data = [
    ('q', [None, True]),
    ('a', [None, False]),
    ('01-21', [datetime.datetime.strptime('01-21','%m-%y').date(), False]),
]
@pytest.mark.parametrize('sample, expected', validate_input_data_test_data)
def test_validate_input_data(sample, expected):
    eh = EdoHandler()
    date_user, end = eh._validate_input_data(sample)

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
    eh = EdoHandler()
    assert eh._validate_dates(date1, date2) == expected

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
    eh = EdoHandler()

    assert eh.get_dates_to_check(date1, date2) == dates

def test_get_exp_str():
    date = datetime.date(2012, 1, 1)
    eh = EdoHandler()
    exp_str = eh.get_exp_str(date)
    
    assert exp_str == '0122'