# We get the information about location / description from user input.
# How do we then get this into an instance of the Event?
# Can we have a CSV with all the countries of the world and then check
# location input against this and get user to ONLY input valid COUNTRY
from pathlib import Path

from humanitarian_management_system import helper
import datetime
import pandas as pd
import tkinter as tk
import tkinter.messagebox


class Event:
    """Essentially creating a humanitarian plan. An 'event' is where
    we add a description etc of where the disaster has happened."""
    # id_arr = []
    event_data = []

    def __init__(self, title, location, description, no_camp, start_date, end_date, ongoing=True):
        self.title = title
        self.location = location
        self.description = description
        self.no_camp = no_camp
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

    def pass_event_info(self, eid):

        if ((self.end_date == None and self.start_date.date() <= datetime.date.today())
                or (self.start_date.date() <= datetime.date.today() and self.end_date.date() >= datetime.date.today())):
            self.ongoing = True
        else:
            self.ongoing = False

        Event.event_data = [
            [eid, self.ongoing, self.title, self.location, self.description, self.no_camp, self.start_date, self.end_date]]
        event_df = pd.DataFrame(Event.event_data,
                                columns=['eid', 'ongoing', 'title', 'location', 'description', 'no_camp', 'startDate',
                                         'endDate'])
        with open('data/eventTesting.csv', 'a') as f:
            event_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

    @staticmethod
    def edit_event_info():
        """
        To edit event information except eid.
        Recognize which event and which column need to be edited,
        then edit by calling each corresponding private function.
        """
        #### In this case, we can 'end an event' by edit this endDate
        df = pd.read_csv('data/eventTesting.csv')
        filtered_df = df[df['ongoing'] == True]
        if filtered_df.empty:
            print("\nThere are no ongoing events to edit.")
            return

        eid_to_edit = ''
        row = -1
        while eid_to_edit == '':
            try:
                Event.display_events(filtered_df)
                eid_to_edit = input('\n--> Enter the event ID to update:')
                if eid_to_edit == 'RETURN':
                    return
                row = df[df['eid'] == int(eid_to_edit)].index[0]
            except IndexError:
                print("\nInvalid event ID entered.")
                eid_to_edit = ''
                continue

        what_to_edit = ''
        while what_to_edit == '':
            try:
                #### Maybe this could be changed into a menu
                what_to_edit = input(
                    '\n--> Choose one to edit (title/ location/ description/ no_camp/ startDate/ endDate):')
                if what_to_edit == 'RETURN':
                    return
                df[what_to_edit]
            except KeyError:
                print("\nInvalid option name entered.")
                what_to_edit = ''
                continue

        if what_to_edit == 'title':
            Event.__change_title(row)
        elif what_to_edit == 'location':
            Event.__change_location(row)
        elif what_to_edit == 'description':
            Event.__change_description(row)
        elif what_to_edit == 'no_camp':
            Event.__change_no_camp(row)
        elif what_to_edit == 'startDate':
            Event.__change_start_date(row)
        else:
            Event.__end_event(row)

    @staticmethod
    def __change_title(row):
        title = input("\n--> Plan title: ")
        if title == 'RETURN':
            return
        helper.modify_csv_value('data/eventTesting.csv', row, 'title', title)
        print("\nPlan title updated.")

    @staticmethod
    def __change_location(row):
        country = []
        country_data = pd.read_csv("data/countries.csv")['name']
        for ele in country_data:
            country.append(ele.lower())
        location = ''
        for ele in country_data:
            country.append(ele.lower())
        while len(location) == 0 and location not in country:
            location = input("\n--> Location(country): ").lower()
            if location == 'RETURN':
                return
            if location not in country:
                print("\nInvalid country name entered")
                location = ''
                continue
        helper.modify_csv_value('data/eventTesting.csv', row, 'location', location)
        print("\nLocation updated.")

    @staticmethod
    def __change_description(row):
        """Option for users to change the description of the event
        in case they made a mistake or the situation escalates etc"""
        description = input("\n--> Description: ")
        if description == 'RETURN':
            return
        helper.modify_csv_value('data/eventTesting.csv', row, 'description', description)
        print("\nDescription updated.")

    @staticmethod
    def __change_no_camp(row):
        while True:
            try:
                no_camp = input("\nCamp Number (positive integers separated by commas): ")
                if no_camp == 'RETURN':
                    return
                if no_camp == 'None':
                    no_camp = None
                    break
                num_list = [int(num) for num in no_camp.split(',')]
                if not all(num > 0 for num in num_list):
                    ## Also no_camp cannot exceed the total number of camps
                    ## Add it after camp.py finished.
                    helper.modify_csv_value('data/eventTesting.csv', row, 'no_camp', no_camp)
                    print("\nCamp number updated.")
                    break
                else:
                    print("\nInvalid camp number entered.")
                    continue
            except ValueError:
                print("\nInvalid camp number entered.")
                continue

    @staticmethod
    def __change_start_date(row):
        """Should this be an option? What would be the implications of this?"""
        #### maybe when the start date is a day in the future, and the user wants to adjust the schedule
        #### Can the start date of an event that has already been started be changed?
        date_format = '%d/%m/%Y'
        df = pd.read_csv('data/eventTesting.csv')
        start_date = datetime.datetime.strptime(df.loc[row]['startDate'], '%Y-%m-%d')
        if start_date.date() <= datetime.date.today() and bool(df.loc[row]['ongoing']) == True:
            print("\nThis event has started, the start date cannot be changed.")
            return
        elif start_date.date() <= datetime.date.today() and bool(df.loc[row]['ongoing']) == False:
            print("\nThis event has been closed.")
            return
        else:
            start_date = ''

        while start_date == '':
            try:
                start_date = input("\n--> Start date (format dd/mm/yy): ")
                if start_date == 'RETURN':
                    return
                start_date = datetime.datetime.strptime(start_date, date_format)
            except ValueError:
                print("\nInvalid date format entered.")
                start_date = ''
                continue
        formatted_start_date = start_date.strftime('%Y-%m-%d')
        helper.modify_csv_value('data/eventTesting.csv', row, 'startDate', formatted_start_date)
        update_ongoing()
        print("\nStart date updated.")

    @staticmethod
    def __end_event(row):
        """How do we prompt a user to be able to input that
        an event has ended? Should we have a small manual for
        the user which says the commands to enter to the command line
        e.g. "end date: dd/mm/yy" will trigger the system to terminate
        the event"""
        # when a user goes to 'end event', we have a pop up
        # which asks 'are you sure' and says that they won't be able to reopen the event
        # after they have ended it, as the requirement says "the
        # humanitarian plan must be closed in the system."
        df = pd.read_csv('data/eventTesting.csv')
        ########### Jess: OR MAYBE HAVE THIS AS ENDDATE LOWER THAN TODAY'S DATE? or some way to make sure we cannot reopen it, as per above...

        #### cannot edit the end date of a closed event
        if (bool(df.loc[row]['ongoing']) == False
                and datetime.datetime.strptime(df['startDate'].loc[row], '%Y-%m-%d').date() <= datetime.date.today()):
            print("\nThis event has been closed.")
        else:
            date_format = '%d/%m/%Y'
            end_date = ''
            while end_date == '':
                try:
                    end_date = input("\n--> End date (format dd/mm/yy): ")
                    if end_date == 'RETURN':
                        return
                    end_date = datetime.datetime.strptime(end_date, date_format)
                except ValueError:
                    print("\nInvalid date format entered.")
                    end_date = ''
                    continue
                if end_date <= datetime.datetime.strptime(df['startDate'].loc[row], '%Y-%m-%d'):
                    print("\nEnd date has to be later than start date.")
                    end_date = ''
                    continue
            if end_date.date() >= datetime.date.today():
                ### if the updated end date is still in the future, then it is still just an update, not an actual closing of...
                ### can probably make the below a bit cleaner but will deal w later
                formatted_end_date = end_date.strftime('%Y-%m-%d')
                helper.modify_csv_value('data/eventTesting.csv', row, 'endDate', formatted_end_date)
                print("\nEnd date updated.")
            else:
                root = tk.Tk()
                result = tk.messagebox.askquestion("Reminder", "Are you sure you want to close the event?")
                if result == "yes":
                    ongoing = False  # set ongoing as false as the plan is no longer active
                    formatted_end_date = end_date.strftime('%Y-%m-%d')
                    helper.modify_csv_value('data/eventTesting.csv', row, 'endDate', formatted_end_date)
                    helper.modify_csv_value('data/eventTesting.csv', row, 'ongoing', ongoing)
                    tk.messagebox.showinfo("Closed successfully", "The event has been successfully closed.")
                else:
                    tk.messagebox.showinfo("Cancel", "The operation to close the event was canceled.")
                root.mainloop()

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

    @staticmethod
    def display_events(df):
        table_str = df.to_markdown(index=False)
        print("\n" + table_str)

    # maybe we can update the 'ongoing' in csv file for each time we run this app
    # by comparing the start and end date with the current date
    # so that the ongoing status will change with the time going
    @staticmethod
    def update_ongoing():
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)
        for index, series in df.iterrows():
            try:
                startDate = datetime.datetime.strptime(str(series['startDate']), '%Y-%m-%d')
            except ValueError: # startDate may exist this error only when entering None in creating an event
                startDate = None
            try:
                endDate = datetime.datetime.strptime(str(series['endDate']), '%Y-%m-%d')
            except ValueError:
                endDate = None

            if ((endDate == None and startDate.date() <= datetime.date.today()) or
                (startDate.date() <= datetime.date.today() and endDate.date() >= datetime.date.today())):
                helper.modify_csv_value(event_csv_path, series['eid']-1, 'ongoing', True)
            else:
                helper.modify_csv_value(event_csv_path, series['eid']-1, 'ongoing', False)

