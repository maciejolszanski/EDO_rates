from attr import Attribute
import requests
import datetime
import os
import csv

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

FIRST_EDO_DATE = datetime.date(2004, 10, 1)
LAST_EDO_DATE = datetime.date.today()


class EdoHandler():
    '''class to manage all the EDO data'''

    def __init__(self):
        self.data_path = r'data/edo_rates.csv'
        self._update_data()

    def _update_data(self):
        '''checks whether the data are stored loccally
           and whether they are up to date'''

        if os.path.exists(self.data_path):
            self.check_updates()
        else:
            print("There are no EDO data stored locally.")
            print("Wait until all the necessary data has been downloaded.")
            self.download_data(FIRST_EDO_DATE)

    def download_data(self, first_date):
        '''creates a directory, downloads the data and stores it in a .csv'''

        dir_name = self.data_path.split('/')[0]
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        dates = self.get_dates_to_check(first_date, LAST_EDO_DATE)

        with open(self.data_path, 'a', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            for i, date in enumerate(dates):
                exp = self.get_exp_str(date)
                rate = self.get_edo_rate(exp)
                writer.writerow([date, rate])
                print(f"Downloaded {i+1}/{len(dates)}")

    def check_updates(self):
        '''checks if the data stored locally are up to date'''
        today = datetime.date.today()

        with open(self.data_path) as f:
            reader = csv.reader(f)
            rows = [row for row in reader]
            last_date_str = rows[-1][0]
            last_d = datetime.datetime.strptime(last_date_str, '%Y-%m-%d')
            # convert datetime to date
            last_d = datetime.date(
                last_d.year, last_d.month, last_d.day)

            if (last_d.year < today.year or
               (last_d.year == today.year and last_d.month < today.month)):
                print("Your local data are out of date.")
                print("Wait until all the necessary data has been downloaded.")
                first_date_to_check = last_d + relativedelta(months=1)
                self.download_data(first_date_to_check)

    def get_edo_rate(self, exp_date_string):
        '''Web scraping for the price of the EDO
           with particular expiration date'''

        url = f'''https://www.obligacjeskarbowe.pl/oferta-obligacji/obligacje-10-letnie-edo/edo{exp_date_string}/'''
        edo_site = requests.get(url).text
        edo_html = BeautifulSoup(edo_site, 'html.parser')

        try:
            rate = edo_html.find(class_='interest').text.split(',')
            rate = float('.'.join(rate))
        except AttributeError:
            print(f"No data for EDO{exp_date_string}, rate = 0% assigned")
            rate = 0

        return rate

    def get_user_dates(self):
        '''Get the dates from the user'''
        end = False

        init_date, end = self.get_single_date('initial')
        fin_date, end = self.get_single_date('final')

        if end or (fin_date is None or init_date is None):
            return None, None, end

        # if the input strings are correct we have to chech if the dates are ok
        valid = self._validate_dates(init_date, fin_date)
        if not valid:
            init_date = None
            fin_date = None

        return init_date, fin_date, end

    def get_single_date(self, adjective):
        '''get a single date from the user'''
        end = False
        date_str = input(f"Pass an {adjective} date as MM-YY:\n")
        date, end = self._validate_input_data(date_str)
        if end or date is None:
            return None, end
        
        return date, end

    def get_dates_to_check(self, init, fin):
        '''creates a list of dates to check EDO rate for'''

        date = init
        dates = []
        while fin - date >= datetime.timedelta(days=0):
            dates.append(date)
            date += relativedelta(months=1)

        return dates

    def get_exp_str(self, date):
        '''converts dates to strings mmyy of expiration date'''

        exp_date = date + relativedelta(years=10)
        month_str = str(exp_date.month)
        if len(month_str) < 2:
            month_str = '0' + month_str
        year_str = str(exp_date.year)
        exp_str = month_str + year_str[-2:]

        return exp_str

    def _validate_input_data(self, date_str):
        '''check if the input data are valid'''

        end = False

        try:
            date = datetime.datetime.strptime(date_str, '%m-%y').date()
        except ValueError:
            if date_str == 'q':
                end = True
                return None, end
            else:
                print('\n')
                print('The format of the dates is incorrect, it should be MM-YY.')
                print('For example: March 2022 should be passed as 03-22.\n')
                print("Let's try again:\n")
                date = None

        return date, end

    def _validate_dates(self, begin, finish):
        '''
        Validate if the initial and final dates are correct
        e.g. the initial date should be earlier than the final date

        When one of the test is not failes it appends False to the 'valid' list
        If ther is any False in the list the function returns false
        '''
        valid = []
        # is the initial date earlier than the final date?
        delta = finish - begin
        if delta > datetime.timedelta(days=0):
            valid.append(True)
        else:
            valid.append(False)
            print('The initial date is later than or equal to the finish date')
            print("Let's try again:\n")

        # is the initial or final date earlier than or equal to today?
        today = datetime.date.today()
        delta_init = today - begin
        delta_fin = today - finish

        if delta_init >= datetime.timedelta(days=0):
            valid.append(True)
        else:
            valid.append(False)
            print(f'The initial date is later than today')
            print("Let's try again:\n")

        if delta_fin >= datetime.timedelta(days=0):
            valid.append(True)
        else:
            valid.append(False)
            print(f'The initial date is later than today')
            print("Let's try again:\n")

        if False in valid:
            return False
        else:
            return True
