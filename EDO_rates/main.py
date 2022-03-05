from logging import raiseExceptions
import requests
import datetime

from bs4 import BeautifulSoup


INFO = '''\nHello!
This program will show you what was the rent of Polish EDO through time.
Follow the instructions below to receive an answer.
(If you would like to quit the program type 'q')
'''

def get_edo_rate(exp_date_string):
    '''Web scraping for the price of the EDO with particular expiration date'''

    url = f'''https://www.obligacjeskarbowe.pl/oferta-obligacji/obligacje-10-letnie-edo/edo{exp_date_string}/'''
    print(url)
    edo_site = requests.get(url).text
    edo_html = BeautifulSoup(edo_site, 'html.parser')

    rate = edo_html.find(class_='interest').text.split(',')
    rate = float('.'.join(rate))

    return rate

def date_to_string(date):
    '''creates a string formated as mmyy from date e/g/ 0322 from 01.03.2022'''
    pass

def get_user_dates():
    '''Get the dates from the user'''
    end = False

    init_str = input("Pass an initial date as MM-YY:\n")
    init_date, end = validate_input_data(init_str)
    if end or init_date is None:
        return None, None, end

    fin_str = input("Pass a final date as MM-YY:\n")
    fin_date, end = validate_input_data(fin_str)
    if end or fin_date is None:
        return None, None, end
    
    # if the input strings are correct we have to chech if the dates are ok
    valid = validate_dates(init_date, fin_date)
    if not valid:
        end = True

    return init_date, fin_date, end

def validate_input_data(date_str):
    '''check if the input data are valid'''

    end = False

    try:
        date = datetime.datetime.strptime(date_str, '%m-%y')
    except ValueError:
        if date_str == 'q':
            end = True
            return None, end
        else:
            print('\nThe format of the dates is incorrect, it should be MM-YY.')
            print('For example: March 2022 should be passed as 03-22.\n')
            print("Let's try again:\n")
            date = None

    return date, end

def validate_dates(begin, finish):
    '''
        validate if the initial and final dates are correct
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
   

if __name__ == '__main__':

    print(INFO)

    while True:
        # ask user about the initial and final date to check EDO rates
        init_date, fin_date, end = get_user_dates()
        if end:
            break
