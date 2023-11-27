# We get the information about location / description from user input.
# How do we then get this into an instance of the Event?
# Can we have a CSV with all the countries of the world and then check
# location input against this and get user to ONLY input valid COUNTRY
from pathlib import Path

import numpy as np

from humanitarian_management_system import helper
import datetime
import pandas as pd
import tkinter as tk
import tkinter.messagebox


class Event:
    """Essentially creating a humanitarian plan. An 'event' is where
    we add a description etc of where the disaster has happened."""

    def __init__(self, title, location, description, no_camp, start_date, end_date, ongoing=True):
        self.title = title
        self.location = location
        self.description = description
        self.no_camp = no_camp
        self.start_date = start_date
        self.end_date = end_date
        self.ongoing = ongoing

    # Access user input info from helper function and pass them into .csv file(s)
    @staticmethod
    def create_new_record(event_info):
        """
        This is the function to create a new event and write new record into csv file.
        """
        # When an event is created after deleting the last row of the event,
        # the new eid will be the same as the eid of the deleted event.
        # To ensure the uniqueness of the event ID, the largest eid ever used is stored.
        # When creating an event, compare this max_used_eid with the eid in event file,
        # take the larger one and add 1 to get the new eid.
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        if pd.read_csv(event_csv_path).empty:
            last_event_id = 0
        else:
            last_event_id = pd.read_csv(event_csv_path)['eid'].max()

        # maxEid_csv_path = Path(__file__).parents[1].joinpath("data/maxUsedEid.csv")
        # max_used_eid = pd.read_csv(maxEid_csv_path)['max_used_eid'].max()
        try:
            event_id = pd.read_csv(event_csv_path)['eid'].max() + 1
        except:
            event_id = 1
        # insert user id into registration_info
        event_info.insert(0, event_id)
        event_df = pd.DataFrame(data=[event_info],
                                columns=['eid', 'ongoing', 'title', 'location', 'description', 'no_camp',
                                         'startDate', 'endDate'])
        event_df.to_csv(event_csv_path, mode='a', index=False, header=False)

        # To prevent confusion caused by directly modifying the eventTesting file
        # use event_id, instead of max_used_eid, add 1 to update max_used_eid
        # max_used_eid = event_id
        # helper.modify_csv_value(maxEid_csv_path, 0, 'max_used_eid', max_used_eid)

    @staticmethod
    def get_all_active_events():
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)
        print(df)
        active_events_df = df[(df['ongoing'] == True) & ((pd.to_datetime(df['endDate']).dt.date >
                                                          datetime.date.today()) | (pd.isna(df['endDate'])))]
        return active_events_df

    @staticmethod
    def edit_event_info():
        """
        To edit event information except eid.
        Recognize which event and which column need to be edited,
        then edit by calling each corresponding private function.
        """
        #### In this case, we can 'end an event' by edit this endDate
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)
        if df.empty:
            print("\nNo events to edit.")
            return
        filtered_df = df[(df['ongoing'] == True) | (df['ongoing'] == 'Yet')]
        if filtered_df.empty:
            print("\nAll the events are closed and cannot be edited.")
            return

        row = -1
        while True:
            try:
                Event.display_events(filtered_df)
                eid_to_edit = input('\n--> Enter the event ID to update:')
                if eid_to_edit == 'RETURN':
                    return
                elif int(eid_to_edit) not in filtered_df['eid'].values:
                    print(f"\nInvalid input! Please enter an integer from {filtered_df['eid'].values} for Event ID.")
                    continue
                else:
                    row = df[df['eid'] == int(eid_to_edit)].index[0]
                    break
            except IndexError:
                print("\nInvalid event ID entered.")
                continue

        while True:
            try:
                #### Maybe this could be changed into a menu
                what_to_edit = input('\n--> Choose one to edit (title/ location/ description/ startDate/ endDate):')
                if what_to_edit == 'RETURN':
                    return
                else:
                    df[what_to_edit]
                    break
            except KeyError:
                print("\nInvalid option name entered.")
                continue

        if what_to_edit == 'title':
            Event.__change_title(row)
        elif what_to_edit == 'location':
            Event.__change_location(row)
        elif what_to_edit == 'description':
            Event.__change_description(row)
        # elif what_to_edit == 'no_camp':
        #     Event.__change_no_camp(row)
        elif what_to_edit == 'startDate':
            Event.__change_start_date(row)
        else:
            Event.__change_end_date(row)

    @staticmethod
    def __change_title(row):
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        title = input("\n--> Plan title: ")
        if title == 'RETURN':
            return
        helper.modify_csv_value(event_csv_path, row, 'title', title)
        print("\nPlan title updated.")

    @staticmethod
    def __change_location(row):
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        country = []
        country_data = pd.read_csv(event_csv_path)['name']
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
        helper.modify_csv_value(event_csv_path, row, 'location', location)
        print("\nLocation updated.")

    @staticmethod
    def __change_description(row):
        """Option for users to change the description of the event
        in case they made a mistake or the situation escalates etc"""
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        description = input("\n--> Description: ")
        if description == 'RETURN':
            return
        helper.modify_csv_value(event_csv_path, row, 'description', description)
        print("\nDescription updated.")
    #
    # @staticmethod
    # def __change_no_camp(row):
    #     event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
    #     while True:
    #         try:
    #             no_camp = input("\n--> Camp Number (positive integers separated by commas): ")
    #             if no_camp == 'RETURN':
    #                 return
    #             elif no_camp == 'NONE':
    #                 helper.modify_csv_value(event_csv_path, row, 'no_camp', None)
    #                 print("\nCamp number updated.")
    #                 break
    #             else:
    #                 num_list = [int(num) for num in no_camp.split(',')]
    #                 if all(num > 0 for num in num_list):
    #                     ## Also no_camp cannot exceed the total number of camps
    #                     ## Add it after camp.py finished.
    #                     num_list = sorted(set(num_list))
    #                     no_camp = ','.join(map(str, num_list))
    #                     helper.modify_csv_value(event_csv_path, row, 'no_camp', no_camp)
    #                     print("\nCamp number updated.")
    #                     break
    #                 else:
    #                     print("\nInvalid camp number entered.")
    #                     continue
    #         except ValueError:
    #             print("\nInvalid camp number entered.")
    #             continue

    @staticmethod
    def __change_start_date(row):
        """Should this be an option? What would be the implications of this?"""
        #### maybe when the start date is a day in the future, and the user wants to adjust the schedule
        #### Can the start date of an event that has already been started be changed?
        date_format = '%d/%m/%Y'
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)

        while True:
            if bool(df.loc[row]['ongoing']) == True:
                print("\nThis event has started, the start date cannot be changed.")
                break
            try:
                start_date = input("\n--> Start date (format dd/mm/yy): ")
                if start_date == 'RETURN':
                    return
                else:
                    start_date = datetime.datetime.strptime(start_date, date_format)
                    formatted_start_date = start_date.strftime('%Y-%m-%d')
                    helper.modify_csv_value(event_csv_path, row, 'startDate', formatted_start_date)
                    Event.update_ongoing()
                    print("\nStart date updated.")
                    break
            except ValueError:
                print("\nInvalid date format entered.")
                continue

    @staticmethod
    def __change_end_date(row):
        """How do we prompt a user to be able to input that
        an event has ended? Should we have a small manual for
        the user which says the commands to enter to the command line
        e.g. "end date: dd/mm/yy" will trigger the system to terminate
        the event"""
        # when a user goes to 'end event', we have a pop up
        # which asks 'are you sure' and says that they won't be able to reopen the event
        # after they have ended it, as the requirement says "the
        # humanitarian plan must be closed in the system."
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)
        date_format = '%d/%m/%Y'
        while True:
            try:
                end_date = input("\n--> End date (format dd/mm/yy): ")
                if end_date == 'RETURN':
                    return
                if end_date == 'NONE':
                    helper.modify_csv_value(event_csv_path, row, 'endDate', None)
                    print("\nEnd date updated.")
                    break
                else:
                    end_date = datetime.datetime.strptime(end_date, date_format)
                    if end_date <= datetime.datetime.strptime(df['startDate'].loc[row], '%Y-%m-%d'):
                        print("\nEnd date has to be later than start date.")
                        continue
                    break
            except ValueError:
                print("\nInvalid date format entered.")
                continue

        if end_date.date() > datetime.date.today():
            formatted_end_date = end_date.strftime('%Y-%m-%d')
            helper.modify_csv_value(event_csv_path, row, 'endDate', formatted_end_date)
            print("\nEnd date updated.")
        else:
            root = tk.Tk()
            result = tk.messagebox.askquestion("Reminder", "Are you sure you want to close the event?")
            if result == "yes":
                ongoing = False
                if df['ongoing'].loc[row] == 'Yet':
                    ongoing = 'Yet'
                elif df['ongoing'].loc[row] == True:
                    ongoing = False
                formatted_end_date = end_date.strftime('%Y-%m-%d')
                helper.modify_csv_value(event_csv_path, row, 'endDate', formatted_end_date)
                helper.modify_csv_value(event_csv_path, row, 'ongoing', ongoing)
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
                helper.modify_csv_value(event_csv_path, index, 'ongoing', True)
            elif startDate.date() > datetime.date.today():
                helper.modify_csv_value(event_csv_path, index, 'ongoing', 'Yet')
            else:
                helper.modify_csv_value(event_csv_path, index, 'ongoing', False)

    @staticmethod
    def disable_ongoing_event():
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)
        filtered_df = df[(df['ongoing'] == True)]

        print("\n*The following shows the info of all available events*")
        Event.display_events(filtered_df)

        eid_to_close = -1
        while True:
            try:
                eid_to_close = input('\n--> Enter the event ID to close:')
                if eid_to_close == 'RETURN':
                    return
                elif int(eid_to_close) not in filtered_df['eid'].values:
                    print(f"\nInvalid input! Please enter an integer from {filtered_df['eid'].values} for Event ID.")
                    continue
                else:
                    break
            except ValueError:
                print("\nInvalid event ID entered.")
                continue
        row = df[df['eid'] == int(eid_to_close)].index[0]
        root = tk.Tk()
        result = tk.messagebox.askquestion("Reminder", "Are you sure you want to close the event?")
        if result == "yes":
            ongoing = False
            helper.modify_csv_value(event_csv_path, row, 'endDate', datetime.date.today())
            helper.modify_csv_value(event_csv_path, row, 'ongoing', ongoing)
            tk.messagebox.showinfo("Closed successfully", "The event has been successfully closed.")
        else:
            tk.messagebox.showinfo("Cancel", "The operation to close the event was canceled.")
        root.mainloop()

    @staticmethod
    def delete_event():
        event_csv_path = Path(__file__).parents[1].joinpath("data/eventTesting.csv")
        df = pd.read_csv(event_csv_path)

        print("\n*The following shows the info of all available events*")
        Event.display_events(df)

        eid_to_delete = -1
        while True:
            try:
                eid_to_delete = input('\n--> Enter the event ID to delete:')
                if eid_to_delete == 'RETURN':
                    return
                elif int(eid_to_delete) not in df['eid'].values:
                    print(f"\nInvalid input! Please enter an integer from {df['eid'].values} for Event ID.")
                    continue
                else:
                    break
            except ValueError:
                print("\nInvalid event ID entered.")
                continue

        root = tk.Tk()
        result = tk.messagebox.askquestion("Reminder", "Are you sure you want to delete the event?")
        if result == "yes":
            df.drop(df[df['eid'] == int(eid_to_delete)].index, inplace=True)
            df.to_csv(event_csv_path, index=False)
            tk.messagebox.showinfo("Closed successfully", "The event has been successfully deleted.")
        else:
            tk.messagebox.showinfo("Cancel", "The operation to delete the event was canceled.")
        root.mainloop()
