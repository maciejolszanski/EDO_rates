import requests
import datetime

from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


class EdoHandler():
    '''class to manage all the EDO data'''

    def __init__(self):
        pass

    def get_edo_rate(self, exp_date_string):
        '''Web scraping for the price of the EDO with particular expiration date'''

        url = f'''https://www.obligacjeskarbowe.pl/oferta-obligacji/obligacje-10-letnie-edo/edo{exp_date_string}/'''
        edo_site = requests.get(url).text
        edo_html = BeautifulSoup(edo_site, 'html.parser')

        rate = edo_html.find(class_='interest').text.split(',')
        rate = float('.'.join(rate))

        return rate


    def get_user_dates(self):
        '''Get the dates from the user'''
        end = False

        init_str = input("Pass an initial date as MM-YY:\n")
        init_date, end = self.validate_input_data(init_str)
        if end or init_date is None:
            return None, None, end

        fin_str = input("Pass a final date as MM-YY:\n")
        fin_date, end = self.validate_input_data(fin_str)
        if end or fin_date is None:
            return None, None, end

        # if the input strings are correct we have to chech if the dates are ok
        valid = self.validate_dates(init_date, fin_date)
        if not valid:
            init_date = None
            fin_date = None

        return init_date, fin_date, end


    def validate_input_data(self, date_str):
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


    def validate_dates(self, begin, finish):
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


    def get_dates_to_check(self, init, fin):
        '''creates a list of dates to check EDO rate for'''

        date = init
        dates = []
        while fin - date >= datetime.timedelta(days=0):
            dates.append(date)
            date += relativedelta(months=1)

        return dates


    def get_exp_str(self, date_list):
        '''converts dates to strings mmyy of expiration date'''
        exp_str_list = []

        for date in date_list:
            exp_date = date + relativedelta(years=10)
            month_str = str(exp_date.month)
            if len(month_str) < 2:
                month_str = '0' + month_str
            year_str = str(exp_date.year)
            exp_str = month_str + year_str[-2:]
            exp_str_list.append(exp_str)

        return exp_str_list
