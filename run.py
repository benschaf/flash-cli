from ast import mod
from pyclbr import _Object
import sys
import os
import random
import time
from typing import Dict, List, NoReturn, Tuple, Union
import gspread
from google.oauth2.service_account import Credentials
import logging
from prettytable import PrettyTable

# Credit for prettytable:
# https://pythonfusion.com/table-on-console-python/#37-terminaltables-or-asciitable

# Credit for error logging:
# https://medium.com/@saadjamilakhtar/5-best-practices-for-python-exception-handling-5e54b876a20
# Credit for formatting of log messages:
# https://docs.python.org/3/howto/logging.html
logging.basicConfig(
    filename="error.log", level=logging.ERROR, format="%(asctime)s %(message)s"
)


# Credit for clear Terminal function:
# https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python


def clear_terminal() -> None:
    """
    Clear function to clean-up the terminal so things don't get messy.
    """
    os.system("cls" if os.name == "nt" else "clear")


# Credit for using the google sheets API:
# https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Credit for exception handling:
# https://medium.com/@saadjamilakhtar/5-best-practices-for-python-exception-handling-5e54b876a20

# Credit for NoReturn type hint:
# https://adamj.eu/tech/2021/05/20/python-type-hints-whats-the-point-of-noreturn/

# Credit for parameter type hints:
# https://stackoverflow.com/questions/2489669/how-do-python-functions-handle-the-types-of-parameters-that-you-pass-in

def handle_exception(e: Exception, message: str) -> NoReturn:
    print(message)
    print(f"Error details: {e}")
    logging.exception(f"{message} Error details: %s", str(e))
    print("Quitting due to error.")
    sys.exit(1)


try:
    print("Loading spreadsheet ...")
    CREDS = Credentials.from_service_account_file("creds.json")
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
    SPREADSHEET_NAME = "flash_cli_sheet"
    SHEET = GSPREAD_CLIENT.open(SPREADSHEET_NAME)
except FileNotFoundError as e:
    handle_exception(e, "Failed to load 'creds.json'. Please ensure the file "
                     "exists in the same directory as this script.")
except ValueError as e:
    handle_exception(e, "Failed to load credentials from 'creds.json'. "
                     "Please ensure that 'creds.json' contains correctly "
                     "formatted credentials for the google API.")
except gspread.exceptions.NoValidUrlKeyFound as e:
    handle_exception(e, "No valid Key was found in 'creds.json'. "
                     "Please ensure that the "
                     "authentication credentials are valid.")
except gspread.exceptions.SpreadsheetNotFound as e:
    handle_exception(e, "Failed to find google spreadsheet: "
                     f"'{SPREADSHEET_NAME}'")
except gspread.exceptions.APIError as e:
    handle_exception(e, "There was an error with the google API.")
except Exception as e:
    handle_exception(e, "An unexpected error occured.")
else:
    clear_terminal()
    print(f"Spreadsheet '{SPREADSHEET_NAME}' successfully loaded!\n")

# Credit for writing docstrings:
# https://www.datacamp.com/tutorial/docstrings-python?utm_source=google&utm_medium=paid_search&utm_campaignid=19589720818&utm_adgroupid=157156373751&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=684592138751&utm_targetid=dsa-2218886984100&utm_loc_interest_ms=&utm_loc_physical_ms=9115817&utm_content=&utm_campaign=230119_1-sea~dsa~tofu_2-b2c_3-eu_4-prc_5-na_6-na_7-le_8-pdsh-go_9-na_10-na_11-na&gad_source=1&gclid=CjwKCAiArLyuBhA7EiwA-qo80DbfmFCbaxqMhOuUbjm3RWcqe_zVQXPxO_LL6__tPOFhAhwsABLhxxoCPqwQAvD_BwE


class Flashcard:
    """
    A class to represent a flashcard.
    """

    def __init__(self, question: str, answer: str, progress_dict: dict):
        self.question = question
        self.answer = answer
        self.progress_dict = progress_dict

    def show_question(self) -> None:
        print(self.question)

    def show_answer(self) -> None:
        print(self.answer)

    def update_progress(self, progress_key: str) -> None:
        self.progress_dict[progress_key] += 1


class Flashcard_Set:
    """
    Represents a set of flashcards.

    Attributes:
        title (str): The title of the flashcard set.
        flashcards (list): A list of Flashcard objects representing
            the flashcards in the set.
    """

    def __init__(self, title: str):
        self.title = title
        self.flashcards = self._load_flashcards()

    def _load_worksheet_data(self) -> List[Dict[str, Union[int, float, str]]]:
        print(f"Loading set from worksheet: '{self.title}'")
        try:
            worksheet = SHEET.worksheet(self.title).get_all_records()
        except gspread.exceptions.WorksheetNotFound as e:
            handle_exception(e, f"The worksheet '{self.title}' "
                             "was not found.")
        except gspread.exceptions.APIError as e:
            handle_exception(e, "An error occurred with the "
                             "Google Sheets API.")
        except Exception as e:
            handle_exception(e, "An unexpected error occurred.")
        else:
            print("Successfully loaded!")
            return worksheet

    def _create_flashcard_from_row(
            self,
            row: Dict[str, Union[int, float, str]]
    ) -> Flashcard:
        question = str(row["question"])
        answer = str(row["answer"])
        progress_dict = {
            "flash_correct": row["flash_correct"],
            "flash_incorrect": row["flash_incorrect"],
            "write_correct": row["write_correct"],
            "write_correct_user_opted": row["write_correct_user_opted"],
            "write_incorrect": row["write_incorrect"],
        }
        return Flashcard(question, answer, progress_dict)

    def _load_flashcards(self) -> List[Flashcard]:
        worksheet_data = self._load_worksheet_data()
        flashcards = [
            self._create_flashcard_from_row(row)
            for row in worksheet_data
        ]
        return flashcards

    def show_all(self) -> None:
        """
        Displays all the flashcards in a table format.
        """
        table = PrettyTable()
        table.field_names = ["Question", "Answer"]
        for flashcard in self.flashcards:
            table.add_row([flashcard.question, flashcard.answer])
        print(f"Showing all flashcards in: '{self.title}'\n")
        print(table)

    def _convert_to_list_of_lists(self) -> list[list]:
        """
        Converts the flashcards into a list of lists.
        A list of lists is needed for the google spreadsheets api.

        Returns:
            list: A list of lists containing the question, answer, and progress
                level of each flashcard.
        """
        li_of_li = []
        for flashcard in self.flashcards:
            tmp_row = [flashcard.question, flashcard.answer]
            for key in flashcard.progress_dict:
                tmp_row.append(flashcard.progress_dict[key])
            li_of_li.append(tmp_row)
        return li_of_li

    def _prepare_data_for_upload(self) -> list:
        headers = [
            "question",
            "answer",
            "flash_correct",
            "flash_incorrect",
            "write_correct",
            "write_correct_user_opted",
            "write_incorrect",
        ]
        flashcard_rows = self._convert_to_list_of_lists()
        data_to_upload = [headers]
        data_to_upload.extend(flashcard_rows)
        return data_to_upload

    def _upload_data_to_worksheet(self, data: list) -> None:
        print(f"\nUploading to worksheet: '{self.title}'...")
        try:
            worksheet = SHEET.worksheet(self.title)
            worksheet.clear()
            worksheet.append_rows(data)
        except gspread.exceptions.WorksheetNotFound as e:
            handle_exception(e, f"The worksheet '{self.title}' was not found.")
        except gspread.exceptions.APIError as e:
            handle_exception(e, "An error occurred with the Google Sheets API.")
        except Exception as e:
            handle_exception(e, "An unexpected error occurred.")
        else:
            print("Successfully uploaded!")

    def upload(self) -> None:
        """
        Uploads the flashcards to the worksheet.
        """
        data_to_upload = self._prepare_data_for_upload()
        self._upload_data_to_worksheet(data_to_upload)

def print_worksheet_titles(worksheets: List[gspread.Worksheet]) -> None:
    for idx in range(1, len(worksheets) + 1):
        print(f"{idx}: {worksheets[idx - 1].title}")

def pick_set() -> Flashcard_Set:
    """
    Prompts the user to pick a set from a list of available sets.

    Returns:
        The selected worksheet converted into a Flahscard_Set object.
    """
    worksheets = SHEET.worksheets()
    while True:
        print("Pick a flashcard set. These are the available sets:")
        print_worksheet_titles(worksheets)
        input_string = input(
            "\nPlease enter the name of the set you'd like to pick, or its "
            f"number (between 1 and {len(worksheets)}): \n"
        )
        while True:
            if input_string == "?":
                clear_terminal()
                break
            # Credit for checking if input string is an int:
            # https://www.w3schools.com/python/ref_func_isinstance.asp
            if input_string.isdigit():
                if int(input_string) in range(1, len(worksheets) + 1):
                    picked_worksheet = worksheets[int(input_string) - 1]
                    return Flashcard_Set(picked_worksheet.title)
            else:
                for worksheet in worksheets:
                    if input_string.lower() == worksheet.title.lower():
                        return Flashcard_Set(worksheet.title)
            input_string = input(
                "Invalid input. "
                f"Please enter a number between 1 and {len(worksheets)}, "
                f"or a valid worksheet name."
                "\nTo see the list of Sets again, enter '?'.\n"
            )


def calculate_percentages(card: Flashcard) -> Tuple[int, int, int]:
    flash_tries = (
        card.progress_dict["flash_correct"] +
        card.progress_dict["flash_incorrect"]
    )
    write_tries = (
        card.progress_dict["write_correct"]
        + card.progress_dict["write_correct_user_opted"]
        + card.progress_dict["write_incorrect"]
    )
    flash_correct_percentage = round(
        card.progress_dict["flash_correct"] / flash_tries * 100
    ) if flash_tries > 0 else 0
    write_correct_percentage = round(
        (card.progress_dict["write_correct"] / write_tries) * 100
    ) if write_tries > 0 else 0
    write_correct_opted_percentage = round(
        (
            (
                card.progress_dict["write_correct_user_opted"]
                + card.progress_dict["write_correct"]
            )
            / write_tries
        )
        * 100
    ) if write_tries > 0 else 0

    return (
        flash_correct_percentage,
        write_correct_percentage,
        write_correct_opted_percentage
    )

def generate_feedback_messages(feedback: str, card: Flashcard) -> Union[List[str], None]:
    (
        flash_correct_percentage,
        write_correct_percentage,
        write_correct_opted_percentage
    ) = calculate_percentages(card)

    if feedback == "flash_correct":
        if flash_correct_percentage == 0:
            return
        return [
            f"Great job! You're part of the {flash_correct_percentage}% "
            "of people who knew the answer!",
            f"You're doing better than {100 - flash_correct_percentage}% "
            "of people who attempted this flashcard.",
            "You knew the answer! Great job!",
        ]
    elif feedback == "flash_incorrect":
        if flash_correct_percentage == 0:
            return
        if flash_correct_percentage < 50:
            return [
                f"Only {flash_correct_percentage}% "
                "of people knew the answer. Keep practicing!",
                "Don't worry, less than half of the people who "
                "attempted this flashcard knew the answer.",
                "Keep practicing!",
            ]
        else:
            return ["Keep practicing!"]
    elif feedback == "write_correct":
        if write_correct_percentage == 0:
            return
        return [
            f"Great job! You're part of the {write_correct_percentage}% "
            "of people who knew the answer!",
            f"You're doing better than {100 - write_correct_percentage}% "
            "of people who attempted this flashcard.",
            "You wrote the correct answer! Great job!",
        ]
    elif feedback == "write_correct_user_opted":
        if write_correct_opted_percentage == 0:
            return
        return [
            f"Great job! You're part of the {write_correct_opted_percentage}% "
            "of people who opted to know the answer or wrote it correctly!",
            f"You're doing better than {100 - write_correct_opted_percentage}%"
            " of people who attempted this flashcard.",
            "Great job! You opted to treat the answer as correct.",
        ]
    elif feedback == "write_incorrect":
        if write_correct_opted_percentage == 0:
            return
        if write_correct_percentage < 50:
            return [
                f"Only {write_correct_percentage}% of people knew the answer. "
                "Keep practicing!",
                "Don't worry, less than half of the people who attempted this "
                "flashcard knew the answer.",
                "You did not write the correct answer. Keep practicing!",
            ]
        else:
            return [
                "You did not write the correct answer. Keep practicing!",
                "Keep practicing!",
                f"{write_correct_opted_percentage}% "
                "of people opted to treat the answer as correct or "
                "wrote it correctly. Keep practicing!",
            ]


def give_feedback_card(card: Flashcard, feedback: str) -> None:
    message_strings = generate_feedback_messages(feedback, card)
    if message_strings is None:
        return
    rnd_idx = random.randint(0, len(message_strings) - 1)
    print(message_strings[rnd_idx])

def determine_mode(answers: dict) -> str:
    if "flash_correct" in answers:
        return "flash_correct"
    else:
        return "write_correct"

def determine_accuracy(set: Flashcard_Set, mode: str, answers: dict) -> int:
    if mode == "flash_correct":
        return round(answers["flash_correct"] / len(set.flashcards) * 100)
    elif mode == "write_correct":
        return round(
            (answers["write_correct"] + answers["write_correct_user_opted"])
            / len(set.flashcards)
            * 100
        )
    else:
        return 0 # This should never happen

def determine_message_strings(
    set: Flashcard_Set,
    mode: str,
    answers: dict,
    accuracy: int
) -> List[str]:
    if accuracy > 50:
        return [
            f"Great job! You got {answers[mode]} out of {len(set.flashcards)} "
            "flashcards correct!",
            f"Congratulations! That makes {accuracy}% right answers!",
        ]
    else:
        return [
            f"You got {answers[mode]} out of {len(set.flashcards)} "
            "flashcards correct!",
            "You can do better! Keep practicing!",
        ]


def give_feedback_set(set: Flashcard_Set, answers: dict) -> None:
    mode = determine_mode(answers)
    accuracy = determine_accuracy(set, mode, answers)
    msg_strs = determine_message_strings(set, mode, answers, accuracy)
    print(msg_strs[0])
    print(msg_strs[1])


def pick_mode() -> str:
    """
    Prompts the user to select a mode and returns the selected mode.

    Returns:
        str: The selected mode.
    """
    modes = {
        "s": "Study with Flashcards",
        "i": "Interactive Quiz",
        "r": "Review All Flashcards",
        "c": "Choose a Different Flashcard Set",
        "?": "Need more details? Just type '?'",
    }
    modes_w_instr = {
        "s": "Study with Flashcards:\n"
        "In this mode, you'll be shown the question side of each card. Try to "
        "answer it in your mind, then press any key to see the answer.\n",
        "i": "Interactive Quiz:\n"
        "In this mode, you'll be shown the question side of each card and "
        "asked to type the answer. Your answer will be checked against the "
        "correct answer.\n",
        "r": "Review All Flashcards:\n"
        "In this mode, you'll see all the questions and answers in the set.\n",
        "c": "Choose a Different Flashcard Set:\n"
        "In this mode, you can go back to the set selection menu to choose a "
        "different set of flashcards to study.\n",
    }
    # Credit for join method:
    # https://docs.python.org/3/library/stdtypes.html#str.join
    modes_keys_str = ", ".join(modes.keys())

    print("\nMAIN MENU\n")
    print("What would you like to do next?")
    for mode, description in modes.items():
        print(f"{mode}: {description}")
    while True:
        # Credit for case insensitive inputs:
        # https://stackoverflow.com/questions/50192965/how-to-make-user-input-not-case-sensitive
        selected_mode = input(f"Select an option ({modes_keys_str}):\n").lower()
        while True:
            if selected_mode in modes:
                if selected_mode == "?":
                    clear_terminal()
                    print("Here are the available options again "
                          "with their descriptions:\n")
                    for mode, description in modes_w_instr.items():
                        print(f"'{mode}' {description}")
                    break
                else:
                    clear_terminal()
                    return selected_mode
            else:
                selected_mode = input(
                    "Invalid input. "
                    f"Please enter one of these letters ({modes_keys_str})\n"
                ).lower()


def input_or_quit(ipt: str) -> str:
    """
    Prompts the user to confirm if they want to quit the program.

    Returns:
        bool: True if the user confirms they want to quit, False otherwise.
    """
    while True:
        user_answer = input(ipt)
        if user_answer.lower() == "q":
            while True:
                user_input = input("Are you sure you want to quit? "
                                   "The progress of this quiz will be "
                                   "lost (y/n)\n").lower()
                if user_input == "y":
                    # wait for 2 seconds before quitting
                    print("Quitting...")
                    # Credit for sleep function:
                    # https://www.datacamp.com/tutorial/python-time-sleep?utm_source=google&utm_medium=paid_search&utm_campaignid=19589720818&utm_adgroupid=157156373751&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=684592138751&utm_targetid=dsa-2218886984100&utm_loc_interest_ms=&utm_loc_physical_ms=9042759&utm_content=&utm_campaign=230119_1-sea~dsa~tofu_2-b2c_3-eu_4-prc_5-na_6-na_7-le_8-pdsh-go_9-na_10-na_11-na&gad_source=1&gclid=Cj0KCQiAoeGuBhCBARIsAGfKY7yufxE5zKBDYxMBH_VoxTSSnHmHTLuVcvkg8bWHAxgocfoWYEecr4oaAt8EEALw_wcB
                    time.sleep(1)
                    return "q"
                elif user_input == "n":
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        else:
            return user_answer


def flashcard_mode(current_set: Flashcard_Set) -> None:
    """
    Run the flashcard mode.

    This function allows the user to go through a set of flashcards, display
    each flashcard's question, show the answer, and update the progress level
    based on the user's response.
    """
    answers = {
        "flash_correct": 0,
        "flash_incorrect": 0,
    }
    for idx in range(len(current_set.flashcards)):
        print("Study with Flashcards\n")
        print(f"Flashcard {idx + 1} / {len(current_set.flashcards)}\n")
        print("Question:")
        current_set.flashcards[idx].show_question()
        ipt = input_or_quit("\nPress Enter to show the Answer "
                            "(or 'q' to quit)\n")
        if ipt is None:
            return
        print("Answer:")
        current_set.flashcards[idx].show_answer()
        print()
        while True:
            answer = input_or_quit("Did you know the Answer? "
                                   "(y, n, q): \n").lower()
            if answer == "q":
                return
            if answer == "y":
                current_set.flashcards[idx].update_progress("flash_correct")
                give_feedback_card(
                    current_set.flashcards[idx], "flash_correct")
                answers["flash_correct"] += 1
                break
            elif answer == "n":
                current_set.flashcards[idx].update_progress("flash_incorrect")
                give_feedback_card(
                    current_set.flashcards[idx], "flash_incorrect")
                answers["flash_incorrect"] += 1
                break
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
        ipt = input_or_quit(
            "\nPress Enter to continue or 'q' to quit\n"
        ).lower()
        if ipt == "q":
            return
        clear_terminal()
    print("Lesson finished\n")
    give_feedback_set(current_set, answers)

    current_set.upload()
    input("\nPress Enter to go back to the main menu\n")


def type_answer_mode(current_set: Flashcard_Set) -> None:
    answers = {
        "write_correct": 0,
        "write_correct_user_opted": 0,
        "write_incorrect": 0,
    }
    for idx in range(len(current_set.flashcards)):
        print("Interactive Quiz")
        print(f"\n\nFlashcard {idx + 1} / {len(current_set.flashcards)}\n")
        print("Question:")
        current_set.flashcards[idx].show_question()
        user_answer = input_or_quit("\nType your Answer (or 'q' to quit):\n")
        if user_answer is None:
            return
        if user_answer == current_set.flashcards[idx].answer:
            print("\nCorrect!")
            current_set.flashcards[idx].update_progress("write_correct")
            give_feedback_card(current_set.flashcards[idx], "write_correct")
            answers["write_correct"] += 1
        else:
            print(
                "\nSeems you have made a mistake.\nCorrect answer: "
                f"{current_set.flashcards[idx].answer}"
            )
            while True:
                correction = input_or_quit(
                    "\nWas your answer correct enough anyways? (y, n, q):\n"
                )
                if correction is None:
                    return
                if correction == "y":
                    print("\nTreating answer as correct.")
                    current_set.flashcards[idx].update_progress(
                        "write_correct_user_opted"
                    )
                    give_feedback_card(
                        current_set.flashcards[idx], "write_correct_user_opted"
                    )
                    answers["write_correct_user_opted"] += 1
                    break
                elif correction == "n":
                    print("\nTreating answer as incorrect.")
                    current_set.flashcards[idx].update_progress(
                        "write_incorrect")
                    give_feedback_card(
                        current_set.flashcards[idx], "write_incorrect")
                    answers["write_incorrect"] += 1
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        input_or_quit("\nPress Enter to continue\n")
        if user_answer is None:
            return
        clear_terminal()
    print("Lesson finished\n")
    give_feedback_set(current_set, answers)
    current_set.upload()
    input("\nPress Enter to go back to the main menu\n")


# Credit to Tim Nelson (CI Mentor) for calling the main function like that.
if __name__ == "__main__":
    """
    This is the main function that controls the flow of the flashcard program.
    It prompts the user to select a mode and then calls the corresponding
    function based on the selected mode.
    """
    print("Welcome to Flashcard CLI!")
    print("This program allows you to practice flashcards and compare your "
          "progress with the Flashcard CLI community.\n")
    while True:
        current_set = pick_set()
        while True:
            clear_terminal()
            print(f"Active Set: {current_set.title}")
            mode = pick_mode()
            if mode == "s":
                flashcard_mode(current_set)
            elif mode == "i":
                type_answer_mode(current_set)
            elif mode == "r":
                # Credit for line break:
                # https://stackoverflow.com/questions/53162/how-can-i-do-a-line-break-line-continuation-in-python-split-up-a-long-line-of
                if not current_set.title.__contains__("not supported"):
                    current_set.show_all()
                else:
                    print("Review mode not supported yet for this set.")
                input("\nPress Enter to go back to the main menu.\n")
            elif mode == "c":
                break
