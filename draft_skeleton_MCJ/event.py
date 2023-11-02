# We get the information about location / description from user input.
# How do we then get this into an instance of the Event?
# Can we have a CSV with all the countries of the world and then check
# location input against this and get user to ONLY input valid COUNTRY
class Event:
    """Essentially creating a humanitarian plan. An 'event' is where
    we add a description etc of where the disaster has happened."""

    def __init__(self, ongoing=True):
        self.location = location
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

    def add_start_date(self):
        """Idea: When the user creates a new "Event" (e.g. instantiates
        a new instance of this class, they are then prompted automatically
        to fill in info about start date (among other attributes), and cannot
        add an event if ay of these are invalid or empty (data integrity)."""

    def add_description(self):
        """Should we limit characters here?"""
        pass

    def end_event(self):
        """How do we prompt a user to be able to input that
        an event has ended? Should we have a small manual for
        the user which says the commands to enter to the command line
        e.g. "end date: dd/mm/yy" will trigger the system to terminate
        the event"""
        # when a user goes to 'end event', we have a pop up
        # which asks 'are you sure' and says that they won't be able to reopen the event
        # after they have ended it, as the requirement says "the
        # humanitarian plan must be closed in the system."
        pass

    def change_description(self):
        """Option for users to change the description of the event
        in case they made a mistake or the situation escalates etc"""
        pass


    def change_start_date(self):
        """Should this be an option? What would be the implications of this?"""
        pass


    def display_humanitarian_plan_summary(self):
        """At any time of the humanitarian plan life cycle, the
        administrator can display summary of all related details; including,
        number of refugees, their camp identification, and number of humanitarian
        volunteers working at each camp."""
#        Again, like the 'end date' option, we could include in a manual a command
#        line command which prompts the system to display the required overview
#       Ideas on where this method should sit? it can be called attached to admin, but
#       relates to everything tracked in event NOT just camp as it refugees from the same
#       disaster can be in many different camps...
        pass
