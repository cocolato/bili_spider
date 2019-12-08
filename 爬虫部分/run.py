import schedule
from get_data import get_data_run

if __name__ == "__main__":

    schedule.every(15).minutes.do(get_data_run, 2019, 11, 19)

    while True:
        schedule.run_pending()

