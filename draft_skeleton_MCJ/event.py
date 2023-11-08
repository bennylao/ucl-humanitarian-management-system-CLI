# We get the information about location / description from user input.
# How do we then get this into an instance of the Event?
# Can we have a CSV with all the countries of the world and then check
# location input against this and get user to ONLY input valid COUNTRY

import helper
import datetime
import pandas as pd


class Event:
    """Essentially creating a humanitarian plan. An 'event' is where
    we add a description etc of where the disaster has happened."""
    id_arr = []
    event_data = []

    def __init__(self, title, location, description, start_date, end_date, ongoing=True):
        self.title = title
        self.location = location
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.ongoing = ongoing

    # def add_start_date(self):
    #     """Idea: When the user creates a new "Event" (e.g. instantiates
    #     a new instance of this class, they are then prompted automatically
    #     to fill in info about start date (among other attributes), and cannot
    #     add an event if ay of these are invalid or empty (data integrity)."""
    #
    # def add_description(self):
    #     """Should we limit characters here?"""
    #     pass

    # Access user input info from helper function and pass them into .csv file(s)
    def pass_event_info(self):
        country = []
        country_data = helper.extract_data("data/countries.csv")['name']
        for ele in country_data:
            country.append(ele)
        date_format = '%d-%m-%Y'  # Use for validating user entered date format

        # keep track of uid and increment it by 1
        try:
            I = helper.extract_data("data/countries.csv")['eid']
        except:
            I = '0'

        for i in I:
            Event.id_arr.append(i)
        eid = Event.id_arr.pop()
        eid = int(eid) + 1

        while len(self.title) == 0:
            self.title = input("--> Plan title: ")

        while len(self.location) == 0 and self.location not in country:
            self.location = input("--> Location(country): ")
            if self.location not in country:
                print("Invalid country name entered")
                self.location = ''
                continue

        while len(self.description) == 0:
            self.description = input("--> Description: ")

        while self.start_date == '':
            try:
                self.start_date = input("--> Start date: ")
                self.start_date = datetime.datetime.strptime(self.start_date, date_format)
            except ValueError:
                print("Invalid date format entered.")
                self.start_date = ''
                continue

        while self.end_date == '':
            try:
                self.end_date = input("--> End date: ")
                self.end_date = datetime.datetime.strptime(self.end_date, date_format)
            except ValueError:
                print("Invalid date format entered.")
                self.end_date = ''
                continue
            if self.end_date <= self.start_date:
                print("End date has to be later than start date.")
                self.end_date = ''
                continue

        Event.event_data = [[eid, self.title, self.location, self.description, 0, self.start_date, self.end_date]]
        event_df = pd.DataFrame(Event.event_data,
                                columns=['eid', 'title', 'location', 'description', 'no_camp', 'startDate', 'endDate'])
        with open('data/eventTesting.csv', 'a') as f:
            event_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

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

    def edit_event_info(selfs):
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
