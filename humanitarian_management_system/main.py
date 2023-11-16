from humanitarian_management_system.models import event
from humanitarian_management_system.models.admin import Admin


def main():
    """This is the function that will run the app."""
    event.Event.update_ongoing()  # update 'ongoing' in event csv file


if __name__ == "__main__":
    # Initialise the creation of the default admin account upon starting the app
    A = Admin('admin', '111', 'xxxxxxxxxxx')
    A.default_account()
    main()