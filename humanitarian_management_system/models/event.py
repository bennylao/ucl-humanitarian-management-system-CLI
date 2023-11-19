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

    def pass_event_info(self, eid):
        # country = []
        # country_data = helper.extract_data("data/countries.csv", "name")
        # for ele in country_data:
        #     country.append(ele.lower())
        # date_format = '%d/%m/%Y'  # Use for validating user entered date format
        #
        # # keep track of uid and increment it by 1
        # try:
        #     I = helper.extract_data("data/eventTesting.csv", "eid")
        # except:
        #     I = '0'
        #
        # for i in I:
        #     Event.id_arr.append(i)
        # eid = 0
        # if Event.id_arr != []:
        #     eid = Event.id_arr.pop()
        # eid = int(eid) + 1
        #
        # while len(self.title) == 0:
        #     self.title = input("--> Plan title: ")
        #     if self.title == 'RETURN':
        #         return
        #
        # while len(self.location) == 0 and self.location not in country:
        #     self.location = input("--> Location(country): ").lower()
        #     if self.location == 'RETURN':
        #         return
        #     if self.location not in country:
        #         print("Invalid country name entered")
        #         self.location = ''
        #         continue
        #
        # while len(self.description) == 0:
        #     self.description = input("--> Description: ")
        #     if self.description == 'RETURN':
        #         return
        #
        # while self.start_date == '':
        #     try:
        #         self.start_date = input("--> Start date (format dd/mm/yy): ")
        #         if self.start_date == 'RETURN':
        #             return
        #         self.start_date = datetime.datetime.strptime(self.start_date, date_format)
        #     except ValueError:
        #         print("Invalid date format entered.")
        #         self.start_date = ''
        #         continue
        #
        # # Maybe not every event has an known end date when it is created,
        # # that's why we need an end_event() function to end it or modify its end date.
        # while self.end_date == '':
        #     try:
        #         self.end_date = input("--> Estimated end date (format dd/mm/yy): ")
        #         if self.end_date == 'RETURN':
        #             return
        #         if self.end_date == 'None':
        #            self.end_date = None
        #            break
        #         self.end_date = datetime.datetime.strptime(self.end_date, date_format)
        #     except ValueError:
        #         print("Invalid date format entered.")
        #         self.end_date = ''
        #         continue
        #     if self.end_date <= self.start_date:
        #         print("End date has to be later than start date.")
        #         self.end_date = ''
        #         continue

        if ((self.end_date == None and self.start_date.date() <= datetime.date.today())
                or (self.start_date.date() <= datetime.date.today() and self.end_date.date() >= datetime.date.today())):
            self.ongoing = True
        else:
            self.ongoing = False

        Event.event_data = [
            [eid, self.ongoing, self.title, self.location, self.description, 0, self.start_date, self.end_date]]
        event_df = pd.DataFrame(Event.event_data,
                                columns=['eid', 'ongoing', 'title', 'location', 'description', 'no_camp', 'startDate',
                                         'endDate'])
        with open('data/eventTesting.csv', 'a') as f:
            event_df.to_csv(f, mode='a', header=f.tell() == 0, index=False)

    def edit_event_info(self):
        """
        To edit event information except eid.
        Recognize which event and which column need to be edited,
        then edit by calling each corresponding private function.
        """
        #### In this case, we can 'end an event' by edit this endDate
        df = pd.read_csv('data/eventTesting.csv')
        eid_to_edit = ''
        row = -1
        while eid_to_edit == '':
            try:
                self.display_events(df)
                eid_to_edit = input('--> Enter the event ID to update:')
                if eid_to_edit == 'RETURN':
                    return
                row = df[df['eid'] == int(eid_to_edit)].index[0]
            except IndexError:
                print("Invalid event ID entered.")
                eid_to_edit = ''
                continue

        what_to_edit = ''
        while what_to_edit == '':
            try:
                #### Maybe this could be changed into a menu
                what_to_edit = input(
                    '--> Choose one to edit (title/ location/ description/ no_camp/ startDate/ endDate):')
                if what_to_edit == 'RETURN':
                    return
                df[what_to_edit]
            except KeyError:
                print("Invalid option name entered.")
                what_to_edit = ''
                continue

        if what_to_edit == 'title':
            self.__change_title(row)
        elif what_to_edit == 'location':
            self.__change_location(row)
        elif what_to_edit == 'description':
            self.__change_description(row)
        elif what_to_edit == 'no_camp':
            self.__change_no_camp(row)
        elif what_to_edit == 'startDate':
            self.__change_start_date(row)
        else:
            self.__end_event(row)

    def __end_event(self, row):
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
            print("This event has been closed.")
        else:
            date_format = '%d/%m/%Y'
            while self.end_date == '':
                try:
                    self.end_date = input("--> End date (format dd/mm/yy): ")
                    if self.end_date == 'RETURN':
                        return
                    self.end_date = datetime.datetime.strptime(self.end_date, date_format)
                except ValueError:
                    print("Invalid date format entered.")
                    self.end_date = ''
                    continue
                if self.end_date <= datetime.datetime.strptime(df['startDate'].loc[row], '%Y-%m-%d'):
                    print("End date has to be later than start date.")
                    self.end_date = ''
                    continue
            if self.end_date.date() >= datetime.date.today():
                ### if the updated end date is still in the future, then it is still just an update, not an actual closing of...
                ### can probably make the below a bit cleaner but will deal w later
                formatted_end_date = self.end_date.strftime('%Y-%m-%d')
                helper.modify_csv_value('data/eventTesting.csv', row, 'endDate', formatted_end_date)
                print("End date updated.")
            else:
                root = tk.Tk()
                result = tk.messagebox.askquestion("Reminder", "Are you sure you want to close the event?")
                if result == "yes":
                    self.ongoing = False  # set ongoing as false as the plan is no longer active
                    formatted_end_date = self.end_date.strftime('%Y-%m-%d')
                    helper.modify_csv_value('data/eventTesting.csv', row, 'endDate', formatted_end_date)
                    helper.modify_csv_value('data/eventTesting.csv', row, 'ongoing', self.ongoing)
                    tk.messagebox.showinfo("Closed successfully", "The event has been successfully closed.")
                else:
                    tk.messagebox.showinfo("Cancel", "The operation to close the event was canceled.")
                root.mainloop()

    def __change_title(self, row):
        self.title = input("--> Plan title: ")
        if self.title == 'RETURN':
            return
        helper.modify_csv_value('data/eventTesting.csv', row, 'title', self.title)
        print("Plan title updated.")

    def __change_location(self, row):
        country = []
        country_data = helper.extract_data("data/countries.csv")['name']
        for ele in country_data:
            country.append(ele.lower())
        while len(self.location) == 0 and self.location not in country:
            self.location = input("--> Location(country): ").lower()
            if self.location == 'RETURN':
                return
            if self.location not in country:
                print("Invalid country name entered")
                self.location = ''
                continue
        helper.modify_csv_value('data/eventTesting.csv', row, 'location', self.location)
        print("Location updated.")

    def __change_description(self, row):
        """Option for users to change the description of the event
        in case they made a mistake or the situation escalates etc"""
        self.description = input("--> Description: ")
        if self.description == 'RETURN':
            return
        helper.modify_csv_value('data/eventTesting.csv', row, 'description', self.description)
        print("Description updated.")

    def __change_no_camp(self, row):
        #### what's the relationship between camp and event?
        pass

    def __change_start_date(self, row):
        """Should this be an option? What would be the implications of this?"""
        #### maybe when the start date is a day in the future, and the user wants to adjust the schedule
        #### Can the start date of an event that has already been started be changed?
        date_format = '%d/%m/%Y'
        df = pd.read_csv('data/eventTesting.csv')
        self.start_date = datetime.datetime.strptime(df.loc[row]['startDate'], '%Y-%m-%d')
        if self.start_date.date() <= datetime.date.today() and bool(df.loc[row]['ongoing']) == True:
            print("This event has started, the start date cannot be changed.")
            return
        elif self.start_date.date() <= datetime.date.today() and bool(df.loc[row]['ongoing']) == False:
            print("This event has been closed.")
            return
        else:
            self.start_date = ''

        while self.start_date == '':
            try:
                self.start_date = input("--> Start date (format dd/mm/yy): ")
                if self.start_date == 'RETURN':
                    return
                self.start_date = datetime.datetime.strptime(self.start_date, date_format)
            except ValueError:
                print("Invalid date format entered.")
                self.start_date = ''
                continue
        formatted_start_date = self.start_date.strftime('%Y-%m-%d')
        helper.modify_csv_value('data/eventTesting.csv', row, 'startDate', formatted_start_date)
        self.update_ongoing()
        print("Start date updated.")

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

    def display_events(self, df):
        # a nice to have to help users navigate... maybe this can be useful later / for other purposes later ?
        # Iterating over each row of the event table, and getting the value from each column
        for i in range(len(df)):
            print(f'''
            +--------------+-------------------+
            | Event ID     | {df.iloc[i]['eid']}
            +--------------+-------------------+
            | Ongoing?     | {df.iloc[i]['ongoing']}
            +--------------+-------------------+
            | Title        | {df.iloc[i]['title']}
            +--------------+-------------------+
            | Location     | {df.iloc[i]['location']}
            +--------------+-------------------+
            | Description  | {df.iloc[i]['description']}
            +--------------+-------------------+
            | # of Camps   | {df.iloc[i]['no_camp']}
            +--------------+-------------------+
            | Start Date   | {df.iloc[i]['startDate']}
            +--------------+-------------------+
            | End Date     | {df.iloc[i]['endDate']}
            +--------------+-------------------+
            ************************************
            ''')

    # I'm not sure whether the ongoing status will change with the time going
    # maybe we can update the 'ongoing' in csv file for each time we run this app
    # by comparing the start and end date with the current date
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

