import gspread
from google.oauth2.service_account import Credentials
# Credit for prettytable: https://pythonfusion.com/table-on-console-python/#37-terminaltables-or-asciitable
from prettytable import PrettyTable
import logging

# Credit for error logging: https://medium.com/@saadjamilakhtar/5-best-practices-for-python-exception-handling-5e54b876a20
# Credit for formatting of log messages: https://docs.python.org/3/howto/logging.html
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(message)s')

# Credit for using the google sheets API goes to Code Institutes love sandwiches project: https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

print("Loading spreadsheet ...")
# Credit for exception handling: https://medium.com/@saadjamilakhtar/5-best-practices-for-python-exception-handling-5e54b876a20
try:
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SPREADSHEET_NAME = "flash_cli_sheet"
    SHEET = GSPREAD_CLIENT.open(SPREADSHEET_NAME)
except FileNotFoundError as e:
    print(f"Failed to load 'creds.json'. Please ensure the file exists in the same directory as this script.")
    print(f"Error details: {e}")
    logging.exception("Failed to load 'creds.json'. Please ensure the file exists in the same directory as this script. Error details: %s", str(e))
except ValueError as e:
    print (f"Failed to load credentials from 'creds.json'. Please ensure that 'creds.json' contains correctly formatted credentials for the google API.")
    print(f"Error details: {e}")
    logging.exception("Failed to load credentials from 'creds.json'. Please ensure that 'creds.json' contains correctly formatted credentials for the google API. Error details: %s", str(e))
except gspread.exceptions.NoValidUrlKeyFound as e:
    print(f"No valid Key was found in 'creds.json'. Please ensure that the authentication credentials are valid.")
    print(f"Error details: {e}")
    logging.exception("No valid Key was found in 'creds.json'. Please ensure that the authentication credentials are valid. Error details: %s", str(e))
except gspread.exceptions.SpreadsheetNotFound as e:
    print(f"Failed to find google spreadsheet: '{SPREADSHEET_NAME}'")
    print(f"Error details: {e}")
    logging.exception("Failed to find google spreadsheet: '%s'. Error details: %s", SPREADSHEET_NAME, str(e))
except gspread.exceptions.APIError as e:
    print(f"There was an error with the google API.")
    print(f"Error details: {e}")
    logging.exception("There was an error with the google API. Error details: %s", str(e))
except Exception as e:
    print(f"An unexpected error occured: {e}")
    logging.exception("An unexpected error occured: %s", str(e))
else:
    print(f"Spreadsheet '{SPREADSHEET_NAME}' successfully loaded!")   

# Credit for writing docstrings: https://www.datacamp.com/tutorial/docstrings-python?utm_source=google&utm_medium=paid_search&utm_campaignid=19589720818&utm_adgroupid=157156373751&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=684592138751&utm_targetid=dsa-2218886984100&utm_loc_interest_ms=&utm_loc_physical_ms=9115817&utm_content=&utm_campaign=230119_1-sea~dsa~tofu_2-b2c_3-eu_4-prc_5-na_6-na_7-le_8-pdsh-go_9-na_10-na_11-na&gad_source=1&gclid=CjwKCAiArLyuBhA7EiwA-qo80DbfmFCbaxqMhOuUbjm3RWcqe_zVQXPxO_LL6__tPOFhAhwsABLhxxoCPqwQAvD_BwE
class Flashcard_Set:
    """
    Represents a set of flashcards.

    Attributes:
        title (str): The title of the flashcard set.
        flashcards (list): A list of Flashcard objects representing the flashcards in the set.
    """

    def __init__(self, title):
        self.title = title
        self.flashcards = self._load_flashcards()

    def _load_flashcards(self):
        """
        Loads the flashcards from the worksheet named like the title Attribute.

        Returns:
            list: A list of Flashcard objects.
        """
        flashcards = []
        worksheet = SHEET.worksheet(self.title).get_all_records()
        for row in worksheet:
            question = row["question"]
            answer = row["answer"]
            mastery_level = row["mastery_level"]
            flashcards.append(Flashcard(question, answer, mastery_level))

        return flashcards

    def show_all(self):
        """
        Displays all the flashcards in a table format.
        """
        table = PrettyTable()
        table.field_names = ["Question", "Answer"]
        
        for flashcard in self.flashcards:
            table.add_row([flashcard.question, flashcard.answer])
        print(table)

    def _convert_to_list_of_lists(self):
        """
        Converts the flashcards into a list of lists.
        A list of lists is needed for the google spreadsheets api.

        Returns:
            list: A list of lists containing the question, answer, and mastery level of each flashcard.
        """
        li_of_li = []
        for flashcard in self.flashcards:
            li_of_li.append([flashcard.question, flashcard.answer, flashcard.mastery_level])
        return li_of_li

    def upload(self):
        """
        Uploads the flashcards to the worksheet.
        """
        data_to_upload = self._convert_to_list_of_lists()

        try:
            worksheet = SHEET.worksheet(self.title)
            worksheet.clear()
            worksheet.append_row(["question", "answer", "mastery_level"])
            worksheet.append_rows(data_to_upload)
        except gspread.exceptions.WorksheetNotFound as e:
            print(f"The worksheet '{self.title}' was not found. Error: {e}")
            logging.exception("The worksheet '%s' was not found: %s", self.title, str(e))
        except gspread.exceptions.APIError as e:
            print(f"An error occurred with the Google Sheets API. Error: {e}")
            logging.exception("An error occurred with the Google Sheets API: %s", str(e))
        except Exception as e:
            print(f"An unexpected error occurred. Error: {e}")
            logging.exception("An unexpected error occurred: %s", str(e))

class Flashcard:
    """
    A class to represent a flashcard.
    """
    def __init__(self, question, answer, mastery_level):
        self.question = question
        self.answer = answer
        self.mastery_level = mastery_level

    # def show_full(self):

    def show_question(self):
        print(self.question)

    def show_answer(self):
        print(self.answer)
    
    def update_mastery(self, increment):
        self.mastery_level += increment

def flashcard_mode():
    """
    Runs the flashcard mode.

    This function loads a flashcard set, displays each flashcard's question, waits for user input to show the answer,
    prompts the user to indicate if they knew the answer, updates the flashcard's mastery level accordingly,
    and finally uploads the flashcard set.

    Returns:
        None
    """
    print("\n\nFlashcard mode")
    print("Loading set...")
    try:
        my_set = Flashcard_Set("flashcards")
    except Exception as e:
        print(f"Failed to load Flashcard Set 'flashcards'. Error: {e}")
        return
    for idx in range(len(my_set.flashcards)):
        print(f"\n\nFlashcard {idx} / {len(my_set.flashcards)}\n")
        print("Question:")
        my_set.flashcards[idx].show_question()
        input("\nPress Enter to show the Answer")
        print("\nAnswer:")
        my_set.flashcards[idx].show_answer()
        print("\n")
        while True:
            answer = input("Did you know the Answer? (y/n): ")
            if answer == "y":
                my_set.flashcards[idx].update_mastery(1)
                break
            elif answer == "n":
                my_set.flashcards[idx].update_mastery(-1)
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
    print("Lesson finished")
    print("Uploading...")
    my_set.upload()
    print("Successfully uploaded.")

def pick_mode():
    """
    Prompts the user to select a mode and returns the selected mode.

    Returns:
        str: The selected mode.
    """
    while True:
        print("f: Flashcard Mode")
        print("t: Type answer Mode")
        # Credit for case insensitive inputs: https://stackoverflow.com/questions/50192965/how-to-make-user-input-not-case-sensitive
        selected_mode = input("Select a mode (f/t): ").lower()
        if selected_mode in ["f", "t"]: 
            return selected_mode
        else:
            print("\nInvalid input. Please enter 'f' or 't'")
    
def main():
    """
    This is the main function that controls the flow of the flashcard program.
    It prompts the user to select a mode and then calls the corresponding function based on the selected mode.
    """
    mode = pick_mode()
    if mode == "f":
        flashcard_mode()
    elif mode == "t":
        type_answer_mode()

main()