import gspread
from google.oauth2.service_account import Credentials
# Credit for prettytable: https://pythonfusion.com/table-on-console-python/#37-terminaltables-or-asciitable
from prettytable import PrettyTable

# Credit for using the google sheets API goes to Code Institutes love sandwiches project: https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('flash_cli_sheet')

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

    def upload(self):
        """
        Uploads the flashcards to the worksheet.
        """
        worksheet = SHEET.worksheet(self.title)
        worksheet.clear()

        data_to_upload = []
        for flashcard in self.flashcards:
            data_to_upload.append([flashcard.question, flashcard.answer, flashcard.mastery_level])

        worksheet.append_row(["question", "answer", "mastery_level"])
        worksheet.append_rows(data_to_upload)

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
    print("Flashcard mode\n")
    print("Loading set...")
    my_set = Flashcard_Set("flashcards")
    for flashcard in my_set.flashcards:
        flashcard.show_question()
        input("Press any key to show the answer")
        flashcard.show_answer()
        answer = input("Did you know the answer? (y/n): ")
        if answer == "y":
            flashcard.update_mastery(1)
        elif answer == "n":
            flashcard.update_mastery(-1)
        print("Next question:")
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
    print("f    Flashcard Mode")
    print("t    Type answer Mode")
    selected_mode = input("Select a mode: ")
    return selected_mode
    
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