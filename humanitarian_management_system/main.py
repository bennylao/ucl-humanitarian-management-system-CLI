import logging
import pathlib
from humanitarian_management_system.controller import Controller
from humanitarian_management_system.models import Event


def main():
    """This is the function that will run the app."""
    Event.update_ongoing()  # update 'ongoing' in event csv file
    log_path = pathlib.Path(__file__).parents[0].joinpath('data/systemLogs.log')
    logging.basicConfig(level=logging.DEBUG,
                        filename=log_path,
                        format='%(asctime)s - %(levelname)s - %(module)s-%(funcName)s-Line%(lineno)d - %(message)s')
    logging.info('Starting Humanitarian Management System')
    c = Controller()
    c.initialise()


if __name__ == "__main__":
    # Initialise the creation of the default admin account upon starting the app
    main()
