import gspread
from google.oauth2.service_account import Credentials

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

class Flashcard_Set:
    def __init__(self, title):
        self.title = title
        self.flashcards = self._load_flashcards()

    def _load_flashcards(self):
        flashcards = []
        worksheet = SHEET.worksheet(self.title).get_all_records()
        for row in worksheet:
            question = row["question"]
            answer = row["answer"]
            mastery_level = row["mastery_level"]
            flashcards.append(Flashcard(question, answer, mastery_level))

        return flashcards
class Flashcard:
    """
    A class to represent a flashcard.
    """
    def __init__(self, question, answer, mastery_level):
        self.question = question
        self.answer = answer
        self.mastery_level = mastery_level

def flashcard_mode():
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
    print("f    Flashcard Mode")
    print("t    Type answer Mode")
    selected_mode = input("Select a mode: ")
    return selected_mode
    
def main():
    mode = pick_mode()
    if mode == "f":
        flashcard_mode()
    elif mode == "t":
        type_answer_mode()

main()