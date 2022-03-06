from shutil import which
import matplotlib.pyplot as plt

def visulise_EDO(dates, rates):

    plt.style.use('classic')
    fig, ax = plt.subplots()
    ax.plot(dates,rates)

    fig.autofmt_xdate()
    ax.set_title('EDO rates', fontsize=22)
    ax.set_ylabel('Rent [%]', fontsize=16)
    ax.set_xlabel('Date of buying EDO', fontsize=16)
    ax.tick_params('both', which='major', labelsize=10)

    plt.show()
