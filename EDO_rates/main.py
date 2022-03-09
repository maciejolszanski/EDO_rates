from EDO_rates.edo_handler import EdoHandler
from EDO_rates.visualise import visulise_EDO

INFO = '''\nHello!
This program will show you what was the rent of Polish EDO through time.
Follow the instructions below to receive an answer.
(If you would like to quit the program type 'q')
'''


if __name__ == '__main__':

    print(INFO)

    eh = EdoHandler()

    while True:
        # ask user about the initial and final date to check EDO rates
        init_date, fin_date, end = eh.get_user_dates()

        # If the 'q' was pressed the functions stops
        if end:
            break
        # When the dates are invalid the while loop starts again
        elif init_date is None or fin_date is None:
            continue

        dates_to_check = eh.get_dates_to_check(init_date, fin_date)
        exp_dates_str = eh.get_exp_str(dates_to_check)

        print('\nCollecting data...')
        rates = []
        for i, exp in enumerate(exp_dates_str):
            rates.append(eh.get_edo_rate(exp))
            print(f"Collected {i+1}/{len(exp_dates_str)}")

        visulise_EDO(dates_to_check, rates)

        break
