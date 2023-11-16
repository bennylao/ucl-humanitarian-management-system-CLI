from humanitarian_management_system.controller import Controller
from humanitarian_management_system.models import event


def main():
    """This is the function that will run the app."""
    event.Event.update_ongoing()  # update 'ongoing' in event csv file
    c = Controller()
    c.initialise()


if __name__ == "__main__":
    # Initialise the creation of the default admin account upon starting the app
    main()
