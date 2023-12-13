from pathlib import Path
from humanitarian_management_system import helper
import datetime
import pandas as pd
import logging


class Event:
    """Essentially creating a humanitarian plan. An 'event' is where
    we add a description etc of where the disaster has happened."""

    def __init__(self, title, location, description, no_camp, start_date, end_date, ongoing):
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
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            if pd.read_csv(event_csv_path, converters={'ongoing': str}).empty:
                last_event_id = 0
            else:
                last_event_id = pd.read_csv(event_csv_path)['eventID'].max()

            max_eid_csv_path = Path(__file__).parents[1].joinpath("data/maxUsedEid.csv")
            max_used_eid = pd.read_csv(max_eid_csv_path)['max_used_eid'].max()
            event_id = max(last_event_id, max_used_eid) + 1
            event_info.insert(0, event_id)
            event_df = pd.DataFrame(data=[event_info],
                                    columns=['eventID', 'ongoing', 'title', 'location', 'description', 'no_camp',
                                             'startDate', 'endDate'])
            event_df.to_csv(event_csv_path, mode='a', index=False, header=False)

            max_used_eid = event_id
            helper.modify_csv_value(max_eid_csv_path, 0, 'max_used_eid', max_used_eid)
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def get_all_active_events():
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})
            print(df)
            active_events_df = df[(df['ongoing'] == 'True') & ((pd.to_datetime(df['endDate']).dt.date >
                                                              datetime.date.today()) | (pd.isna(df['endDate'])))]
            return active_events_df
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def edit_event_info():
        """
        To edit event information except eid.
        Recognize which event and which column need to be edited,
        then edit by calling each corresponding private function.
        """
        sign = 0
        sign2 = 0
        sign3 = 0
        try:
            while sign3 == 0:
                event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
                df = pd.read_csv(event_csv_path, converters={'ongoing': str})
                if df.empty:
                    print("\nNo events to edit.")
                    return
                filtered_df = df[(df['ongoing'] == 'True') | (df['ongoing'] == 'Yet')]
                if filtered_df.empty:
                    print("\nAll the events are closed and cannot be edited.")
                    return

                while sign2 == 0:
                    try:
                        Event.display_events(filtered_df)
                        eid_to_edit = input('\n--> Enter the event ID to update:')
                        if eid_to_edit == 'RETURN':
                            return
                        elif int(eid_to_edit) not in filtered_df['eventID'].values:
                            print(
                                f"\nInvalid input! Please enter an integer from {filtered_df['eventID'].values} for Event ID.")
                            continue
                        else:
                            row = df[df['eventID'] == int(eid_to_edit)].index[0]
                            event_id = int(eid_to_edit)
                            break
                    except IndexError:
                        print("\nInvalid event ID entered.")
                        continue
                    except ValueError:
                        print("\nInvalid event ID entered.")
                        continue

                while sign == 0:
                    try:
                        what_to_edit = input("\nChoose one to edit\n"
                                             "[ 1 ] title\n"
                                             "[ 2 ] location\n"
                                             "[ 3 ] description\n"
                                             "[ 4 ] start date\n"
                                             "[ 5 ] end date\n"
                                             "[ R ] Return to the previous page\n"
                                             "--> ")
                        if what_to_edit == 'RETURN' or what_to_edit == 'R':
                            return
                        elif int(what_to_edit) not in [1,2,3,4,5]:
                            print("\nInvalid input! Please choose one from 1 to 5.")
                            continue
                        else:
                            if what_to_edit == '1':
                                Event.__change_title(row)
                            elif what_to_edit == '2':
                                Event.__change_location(row)
                            elif what_to_edit == '3':
                                Event.__change_description(row)
                            elif what_to_edit == '4':
                                Event.__change_start_date(row)
                            elif what_to_edit == '5':
                                Event.__change_end_date(row, event_id)
                            df1 = pd.read_csv(event_csv_path)
                            Event.display_events(df1.loc[df['eventID'] == int(eid_to_edit)])
                            break
                    except Exception:
                        print("\nInvalid index entered.")
                        continue

                while True:
                    whether_continue = input("\nDo you want to continue editing this event? (yes/no) ").lower()
                    if whether_continue == 'return':
                        return
                    elif whether_continue == 'yes':
                        sign = 0
                        sign2 = 1
                        break
                    elif whether_continue == 'no':
                        whether_another = input("\nDo you want to continue editing another event? (yes/no) ").lower()
                        if whether_another == 'yes':
                            sign2 = 0
                            sign = 0
                            break
                        elif whether_another == 'no':
                            sign2 = 1
                            sign = 1
                            sign3 = 1
                            break
                        else:
                            print("\nPlease enter yes or no.")
                            continue
                    else:
                        print("\nPlease enter yes or no.")
                        continue
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def __change_title(row):
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            title = input("\n--> Plan title: ")
            if title == 'RETURN':
                return
            helper.modify_csv_value(event_csv_path, row, 'title', title)
            print("\n\u2714 Plan title updated.")
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def __change_location(row):
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            countries_csv_path = Path(__file__).parents[1].joinpath("data/country.csv")
            df_countries = pd.read_csv(countries_csv_path)
            df_countries['name'] = df_countries['name'].str.lower()
            country = df_countries['name'].tolist()
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})
            if df['no_camp'][row] == 0:
                while True:
                    location = input("\n--> Location(country): ").lower()
                    if location.upper() == 'RETURN':
                        return
                    elif location not in country:
                        print("\nInvalid country name entered")
                        location = ''
                        continue
                    else:
                        break
                country_id = df_countries.loc[df_countries['name'] == location, 'countryID'].values[0]
                df_countries = pd.read_csv(countries_csv_path)
                location = df_countries.loc[df_countries['countryID'] == country_id, 'name'].values[0]
                helper.modify_csv_value(event_csv_path, row, 'location', location)
                print("\n\u2714 Location updated.")
            else:
                print("\nThere are camps created in this event. The location of event cannot be changed.")
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def __change_description(row):
        """Option for users to change the description of the event
        in case they made a mistake or the situation escalates etc"""
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            description = input("\n--> Description: ")
            if description == 'RETURN':
                return
            helper.modify_csv_value(event_csv_path, row, 'description', description)
            print("\n\u2714 Description updated.")
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def __change_start_date(row):
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})
            date_format = '%d/%m/%Y'
            while True:
                if df.loc[row]['ongoing'] == 'True':
                    print("\nThis event has started, the start date cannot be changed.")
                    break
                try:
                    # start_date = input("\n--> Start date (format dd/mm/yyyy): ")
                    print("\n--> Start date (format dd/mm/yyyy): ")
                    start_date = helper.not_too_old()
                    if start_date == 'RETURN':
                        return
                    else:
                        start_date = datetime.datetime.strptime(start_date, date_format)
                        formatted_start_date = start_date.strftime('%Y-%m-%d')
                        helper.modify_csv_value(event_csv_path, row, 'startDate', formatted_start_date)
                        Event.update_ongoing()
                        print("\n\u2714 Start date updated.")
                        break
                except ValueError:
                    print("\nInvalid date format entered.")
                    continue
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def __change_end_date(row, eid):
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})
            date_format = '%d/%m/%Y'
            while True:
                try:
                    end_date = input("\n--> End date (format dd/mm/yyyy): ")
                    if end_date == 'RETURN':
                        return
                    if end_date == 'NONE':
                        helper.modify_csv_value(event_csv_path, row, 'endDate', None)
                        print("\n\u2714 End date updated.")
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
            if end_date == 'NONE':
                return
            elif end_date.date() > datetime.date.today():
                formatted_end_date = end_date.strftime('%Y-%m-%d')
                helper.modify_csv_value(event_csv_path, row, 'endDate', formatted_end_date)
                print("\n\u2714 End date updated.")
            else:
                camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
                df_camp = pd.read_csv(camp_csv_path)
                row_camp_list = df_camp[
                    (df_camp['eventID'] == df.loc[row, 'eventID']) & (df_camp['status'] == 'open')].index.tolist()
                while True:
                    result = input("\n*** Are you sure you want to close the event? You'll also close the camps in that event.\n"
                                   "--> yes/no ").lower()
                    if result == "yes":
                        ongoing = 'False'
                        if df['ongoing'].loc[row] == 'Yet':
                            ongoing = 'Yet'
                        elif df['ongoing'].loc[row] == 'True':
                            ongoing = 'False'
                        formatted_end_date = end_date.strftime('%Y-%m-%d')
                        helper.modify_csv_value(event_csv_path, row, 'endDate', formatted_end_date)
                        helper.modify_csv_value(event_csv_path, row, 'ongoing', ongoing)
                        if row_camp_list:
                            for row_camp in row_camp_list:
                                helper.modify_csv_value(camp_csv_path, row_camp, 'status', 'closed')
                        refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
                        ref_df = pd.read_csv(refugee_csv_path)
                        camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
                        camp_df = pd.read_csv(camp_csv_path)
                        camp_df.loc[df_camp['eventID'] == int(eid), 'refugeePop'] = 0
                        camp_df.to_csv(camp_csv_path, index=False)
                        camps_in_event = camp_df.loc[camp_df['eventID'] == eid, 'campID'].tolist()
                        rid_list = []
                        for camp in camps_in_event:
                            rids = ref_df.loc[ref_df['campID'] == camp]['refugeeID'].tolist()
                            rid_list.extend(rids)
                        for rid in rid_list:
                            medical_info_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/medicalInfo.csv"))
                            medical_info_df.drop(medical_info_df[medical_info_df['refugeeID'] == int(rid)].index,
                                                 inplace=True)
                            medical_info_df.reset_index(drop=True, inplace=True)
                            medical_info_df.to_csv(Path(__file__).parents[1].joinpath("data/medicalInfo.csv"),
                                                   index=False)
                        for i in camps_in_event:
                            ref_df.drop(ref_df[ref_df['campID'] == i].index, inplace=True)
                        ref_df.reset_index(drop=True, inplace=True)
                        ref_df.to_csv(refugee_csv_path, index=False)
                        print("\n\u2714 The event has been successfully closed.")
                        break
                    elif result == "no":
                        print("\n***  The operation to close the event was canceled.  ***")
                        break
                    elif result == "RETURN":
                        return
                    else:
                        print("\nYou need to choose between 'yes/no'.")
                        continue
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def display_events(df):
        table_str = df.to_markdown(index=False)
        print("\n" + table_str)

    @staticmethod
    def update_ongoing():
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})
            camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
            df_camp = pd.read_csv(camp_csv_path)
            for index, series in df.iterrows():
                try:
                    start_date = datetime.datetime.strptime(str(series['startDate']), '%Y-%m-%d')
                except ValueError:
                    start_date = None
                try:
                    end_date = datetime.datetime.strptime(str(series['endDate']), '%Y-%m-%d')
                except ValueError:
                    end_date = None

                if ((end_date == None and start_date.date() <= datetime.date.today()) or
                        (start_date.date() <= datetime.date.today() and end_date.date() > datetime.date.today())):
                    helper.modify_csv_value(event_csv_path, index, 'ongoing', 'True')
                elif start_date.date() > datetime.date.today():
                    helper.modify_csv_value(event_csv_path, index, 'ongoing', 'Yet')
                else:
                    helper.modify_csv_value(event_csv_path, index, 'ongoing', 'False')
                    row_camp_list = df_camp[
                        (df_camp['eventID'] == df.loc[index, 'eventID']) & (df_camp['status'] == 'open')].index.tolist()
                    if row_camp_list:
                        for row_camp in row_camp_list:
                            helper.modify_csv_value(camp_csv_path, row_camp, 'status', 'closed')
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def disable_ongoing_event():
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})
            camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
            df_camp = pd.read_csv(camp_csv_path)
            filtered_df = df[(df['ongoing'] == 'True')]

            print("\n*The following shows the info of all available events*")
            Event.display_events(filtered_df)

            eid_to_close = -1
            while True:
                try:
                    eid_to_close = input('\n--> Enter the event ID to close:')
                    if eid_to_close == 'RETURN':
                        return
                    elif int(eid_to_close) not in filtered_df['eventID'].values:
                        print(f"\nInvalid input! Please enter an integer from {filtered_df['eventID'].values} for Event ID.")
                        continue
                    else:
                        break
                except IndexError:
                    print("\nInvalid event ID entered.")
                    continue
                except ValueError:
                    print("\nInvalid event ID entered.")
                    continue

            row = df[df['eventID'] == int(eid_to_close)].index[0]
            row_camp_list = df_camp[
                (df_camp['eventID'] == int(eid_to_close)) & (df_camp['status'] == 'open')].index.tolist()
            while True:
                result = input("\n*** Are you sure you want to close the event? You'll also close the camps "
                               "and delete the refugees in that event.\n"
                               "--> yes/no ").lower()
                if result == "yes":
                    ongoing = 'False'
                    helper.modify_csv_value(event_csv_path, row, 'endDate', datetime.date.today())
                    helper.modify_csv_value(event_csv_path, row, 'ongoing', ongoing)
                    if row_camp_list:
                        df_camp.loc[df_camp['eventID'] == int(eid_to_close), 'status'] = 'closed'
                        df_camp.loc[df_camp['eventID'] == int(eid_to_close), 'refugeePop'] = 0
                        df_camp.to_csv(camp_csv_path, index=False)
                    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
                    ref_df = pd.read_csv(refugee_csv_path)
                    camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
                    camp_df = pd.read_csv(camp_csv_path)
                    camps_in_event = camp_df.loc[camp_df['eventID'] == int(eid_to_close), 'campID'].tolist()
                    rid_list = []
                    for camp in camps_in_event:
                        rids = ref_df.loc[ref_df['campID'] == camp]['refugeeID'].tolist()
                        rid_list.extend(rids)
                    for rid in rid_list:
                        medical_info_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/medicalInfo.csv"))
                        medical_info_df.drop(medical_info_df[medical_info_df['refugeeID'] == int(rid)].index, inplace=True)
                        medical_info_df.reset_index(drop=True, inplace=True)
                        medical_info_df.to_csv(Path(__file__).parents[1].joinpath("data/medicalInfo.csv"), index=False)
                    for i in camps_in_event:
                        ref_df.drop(ref_df[ref_df['campID'] == i].index, inplace=True)
                    ref_df.reset_index(drop=True, inplace=True)
                    ref_df.to_csv(refugee_csv_path, index=False)
                    print("\n\u2714 The event has been successfully closed.")
                    break
                elif result == "no":
                    print("\n***  The operation to close the event was canceled.  ***")
                    break
                elif result == "RETURN":
                    return
                else:
                    print("\nYou need to choose between 'yes/no'.")
                    continue
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")

    @staticmethod
    def delete_event():
        try:
            event_csv_path = Path(__file__).parents[1].joinpath("data/event.csv")
            df = pd.read_csv(event_csv_path, converters={'ongoing': str})

            print("\n*The following shows the info of all available events*")
            Event.display_events(df)

            eid_to_delete = -1
            while True:
                try:
                    eid_to_delete = input('\n--> Enter the event ID to delete:')
                    if eid_to_delete == 'RETURN':
                        return
                    elif int(eid_to_delete) not in df['eventID'].values:
                        print(f"\nInvalid input! Please enter an integer from {df['eventID'].values} for Event ID.")
                        continue
                    else:
                        break
                except IndexError:
                    print("\nInvalid event ID entered.")
                    continue
                except ValueError:
                    print("\nInvalid event ID entered.")
                    continue
            while True:
                result = input("*** Are you sure you want to delete the event? "
                               "You'll also close the camps and lose all the information about the refugees in that event.\n"
                               "--> yes/no ").lower()
                if result == "yes":
                    df.drop(df[df['eventID'] == int(eid_to_delete)].index, inplace=True)
                    df.to_csv(event_csv_path, index=False)
                    # --------- added logic to delete refugees in this event -----------------
                    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
                    ref_df = pd.read_csv(refugee_csv_path)
                    camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
                    camp_df = pd.read_csv(camp_csv_path)
                    camp_df.loc[camp_df['eventID'] == int(eid_to_delete), 'refugeePop'] = 0
                    camp_df.to_csv(camp_csv_path, index=False)
                    camps_in_event = camp_df.loc[camp_df['eventID'] == int(eid_to_delete), 'campID'].tolist()
                    rid_list = []
                    for camp in camps_in_event:
                        rids = ref_df.loc[ref_df['campID'] == camp]['refugeeID'].tolist()
                        rid_list.extend(rids)
                    for rid in rid_list:
                        medical_info_df = pd.read_csv(Path(__file__).parents[1].joinpath("data/medicalInfo.csv"))
                        medical_info_df.drop(medical_info_df[medical_info_df['refugeeID'] == int(rid)].index, inplace=True)
                        medical_info_df.reset_index(drop=True, inplace=True)
                        medical_info_df.to_csv(Path(__file__).parents[1].joinpath("data/medicalInfo.csv"), index=False)
                    for i in camps_in_event:
                        ref_df.drop(ref_df[ref_df['campID'] == i].index, inplace=True)
                    ref_df.reset_index(drop=True, inplace=True)
                    ref_df.to_csv(refugee_csv_path, index=False)

                    # reset volunteer camp, role and event info after event is deleted
                    vol_csv_path = Path(__file__).parents[1].joinpath("data/user.csv")
                    vol_df = pd.read_csv(vol_csv_path)
                    vol_df.loc[vol_df['campID'].isin(camps_in_event), 'campID'] = 0
                    vol_df.to_csv(vol_csv_path)

                    row_camp_list = camp_df[
                        (camp_df['eventID'] == int(eid_to_delete)) & (camp_df['status'] == 'open')].index.tolist()
                    if row_camp_list:
                        for row_camp in row_camp_list:
                            helper.modify_csv_value(camp_csv_path, row_camp, 'status', 'closed')
                    print("\n\u2714 The event has been successfully deleted.")
                    break
                elif result == "no":
                    print("\n***  The operation to delete the event was canceled.  ***")
                    break
                elif result == "RETURN":
                    return
                else:
                    print("\nYou need to choose between 'yes/no'.")
                    continue
        except FileNotFoundError as e:
            print(f"\nFile not found."
                  f"\nPlease contact admin for further assistance."
                  f"\n[Error] {e}")
            logging.critical(f"{e}")