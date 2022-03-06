import matplotlib.pyplot as plt
import datetime

def visulise_EDO(dates, rates):

    dates = _convert_dates_to_datetimes(dates)
    
    plt.style.use('classic')
    fig, ax = plt.subplots()
    ax.plot(dates,rates)

    fig.autofmt_xdate()
    ax.set_title('EDO rates', fontsize=22)
    ax.set_ylabel('Rent [%]', fontsize=16)
    ax.set_xlabel('Date of buying EDO', fontsize=16)
    ax.tick_params('both', which='major', labelsize=10)

    plt.show()

def _convert_dates_to_datetimes(dates):
    '''Only for estetic purposes - it is better displayed by matplotlib'''

    datetimes = []
    for date in dates:
        datetimes.append(datetime.datetime(date.year, date.month, date.day))

    return datetimes