import pytest
from EDO_rates.main import *

def test_get_edo_rate():
    assert get_edo_rate('1231') == 1.7