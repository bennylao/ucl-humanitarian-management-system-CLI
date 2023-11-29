from pathlib import Path
import pandas as pd
import csv
from humanitarian_management_system import helper
from datetime import datetime


def create_training_session():
    training_session_path = Path(__file__).parents[1].joinpath("data/trainingSessions.csv")
    session_df = pd.read_csv(training_session_path)
    role_type_path = Path(__file__).parents[1].joinpath("data/roleType.csv")
    role_df = pd.read_csv(role_type_path)
    camp_csv_path = Path(__file__).parents[1].joinpath("data/camp.csv")
    camp_df = pd.read_csv(camp_csv_path)
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    ref_df = pd.read_csv(refugee_csv_path)
    print(role_df.to_string(index=False))
    while True:
        occupation = input("\nFrom the list above enter the role which is closest to your own"
                           "\n or enter RETURN to exit: ")
        if occupation.lower() == "return":
            return
        elif role_df['name'].eq(occupation.lower()).any():
            break
        else:
            print("\nSorry - that role doesn't exist in our system. Pick again or enter RETURN: ")
    while True:
        topic = input("\nEnter the type of topic you will be discussing in your skills session: ")
        if topic.lower() == "return":
            return
        else:
            break
    while True:
        date_input = input("\nEnter the date of the session (e.g., YYYY-MM-DD): ")
        if date_input.lower() == "return":
            return
        else:
            try:
                date = datetime.strptime(date_input, '%Y-%m-%d').date()
                if date > datetime.now().date():
                    break
                else:
                    print("Can't select a date in the past! Try again.")
            except ValueError:
                print("\nInvalid date format. Please use the format YYYY-MM-DD. Or enter RETURN to quit.")
    while True:
        camp = input("\nEnter the campID of the camp you will be holding the session at: ")
        if camp.lower() == "return":
            return
        elif camp_df['campID'].eq(int(camp)).any():
            break
        else:
            print("\nSorry - that role doesn't exist in our system. Pick again or enter RETURN.")
    print(ref_df)

    participants = []
    while True:
        rid = input(
            "\nFrom the list above, one at a time enter a refugee ID for who shall be joining the skills session"
            "\n or enter RETURN to stop: ")
        if rid.lower() == 'return':
            break
        elif rid in participants:
            print("You've already added that refugee!")
        elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
            participants.append(rid)
        else:
            print("\nSorry - that refugee ID doesn't exist. Pick again.")

#     Now we have all the info we need to create a training session
# Need to also increment sessionID by 1.
    print(f"Here is a confirmed list of the refugees you have selected to attend. You can add more later: ")
    for participant in participants:
        print(participant)
    print("Great! That's all the info we need to create a session. ")
    session_arr = pd.read_csv(training_session_path)["sessionID"].tolist()
    if len(session_arr) == 0:
        sessionID = 0
    else:
        sessionID = int(session_arr.pop())
    sessionID += 1

    training_session_data = [int(sessionID), occupation, topic, date, camp, participants]
    session_df.loc[len(session_df)] = training_session_data
    session_df.to_csv(training_session_path, index=False)

# Need to add this in volunteer menu
# Need to add simple one to controller which calls back to appropriate reutrn nmenu
# Add to helper once working.
# create_training_session()



def add_refugee_to_session():
    refugee_csv_path = Path(__file__).parents[1].joinpath("data/refugee.csv")
    ref_df = pd.read_csv(refugee_csv_path)
    training_session_path = Path(__file__).parents[1].joinpath("data/trainingSessions.csv")
    session_df = pd.read_csv(training_session_path)
    print("It's great another refugee wants to join a skills session!")
    print(session_df.to_string(index=False))
    while True:
        sessionID = input("\n\nFrom the list above, enter the session ID for the "
                          "skills session you want to add more participants to. Or enter RETURN to go back: ")
        if sessionID.lower() == 'return':
            return
        elif sessionID.strip() and sessionID.strip().isdigit() and session_df['sessionID'].eq(int(sessionID)).any():
            break
        else:
            print("\n\nSorry - that's not a valid session ID. Pick again. ")
    print(ref_df.to_string(index=False))
    row_index_sessionID = session_df[session_df['sessionID'] == int(sessionID)].index[0]
    already_registered = session_df.at[row_index_sessionID, 'participants']
    participants = []
    while True:
        rid = input(f"\n\nFrom the above list, enter the Refugee ID for who you want to add to session {sessionID}"
                    "\nEnter STOP when you are finished, or return to go back: ")
        if rid.lower() == "return":
            return
        if rid.lower() == 'stop':
            break
        elif rid in already_registered:
            print(f"\nDon't worry. That refugee is already down to attend this session.")
        elif rid in participants:
            print("\nYou've already just added that refugee.")
        elif rid.strip() and rid.strip().isdigit() and ref_df['refugeeID'].eq(int(rid)).any():
            print(f"\n\nAdding refugee with id {rid} to skills session {sessionID}. ")
            participants.append(rid)
        else:
            print("\n\nSorry - that refugee ID doesn't exist. Pick again.")

    # Now we need to add the new "participants" list to the participants list in the csv for the right session
    combined_attendees = [already_registered] + participants
    session_df.at[row_index_sessionID, 'participants'] = combined_attendees
    session_df.to_csv(training_session_path, index=False)
    print(f"\nExcellent! We have added refugees {participants} to session {sessionID}. See below. ")
    print(session_df.to_string(index=False))
add_refugee_to_session()


def delete_session():
    training_session_path = Path(__file__).parents[1].joinpath("data/trainingSessions.csv")
    session_df = pd.read_csv(training_session_path)
    print("\nLooks like you want to cancel or delete a session. That's a shame! ")
    while True:
        sessionID = input("Enter RETURN now if you have changed your mind, or enter the sessionID you"
                          "\n want to cancel: ")
        if sessionID.lower() == 'return':
            return
        elif sessionID.strip() and sessionID.strip().isdigit() and session_df['sessionID'].eq(int(sessionID)).any():
            break
        else:
            print("\n\nSorry - that's not a valid session ID. Pick again. ")
    session_date = session_df.at[sessionID, 'date']
    session_datetime = datetime.strptime(session_date, '%Y-%m-%d').date()
    if session_datetime < datetime.now().date():
        while True:
            confirm = input("\nYou're about to delete a previously given skills session. "
                       "\nEnter YES to confirm or RETURN to cancel: ")
            if confirm.lower == 'return':
                return
            elif confirm.lower() == 'yes':
                break
            else:
                print("Invalid option. Try again.")
    else:
        while True:
            confirm = input("\nYou're about to cancel an skills session that hasn't yet been given. "
                            "\nAre you sure? Enter YES to confirm or RETURN to cancel: ")
            if confirm.lower == 'return':
                return
            elif confirm.lower() == 'yes':
                break
            else:
                print("\nInvalid option. Try again.")
    #Update CSV files accordingly
    session_df.drop(session_df[session_df['refugeeID'] == int(sessionID)].index, inplace=True)
    session_df.to_csv(training_session_path, index=False)







