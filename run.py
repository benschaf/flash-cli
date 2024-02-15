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

class Flashcard:
    """
    A class to represent a flashcard.
    """
    def __init__(self, question, answer, mastery_level):
        self.question = question
        self.answer = answer
