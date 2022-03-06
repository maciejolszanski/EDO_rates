import pytest
from EDO_rates.visualise import *
import datetime

@pytest.fixture
def dates():
    date1 = datetime.date(2012, 1, 1)
    date2 = datetime.date(2012, 2, 1)
    date3 = datetime.date(2012, 3, 1)

    dates = [date1, date2, date3]

    return dates

def test_convert_to_datetimes(dates):
    
    dt1 = datetime.datetime(2012, 1, 1)
    dt2 = datetime.datetime(2012, 2, 1)
    dt3 = datetime.datetime(2012, 3, 1)
    datetimes = [dt1, dt2, dt3] 
    
    assert convert_dates_to_datetimes(dates) == datetimes

