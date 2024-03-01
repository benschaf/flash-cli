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
    Clears the terminal screen.

    This function is used to clear the terminal screen. It uses the os specific
    command to clear the terminal screen. It uses 'cls' for windows and 'clear'
    for linux and mac.
    """
    os.system("cls" if os.name == "nt" else "clear")


# Credit for exception handling:
# https://medium.com/@saadjamilakhtar/5-best-practices-for-python-exception-handling-5e54b876a20

# Credit for NoReturn type hint:
# https://adamj.eu/tech/2021/05/20/python-type-hints-whats-the-point-of-noreturn/

# Credit for parameter type hints:
# https://stackoverflow.com/questions/2489669/how-do-python-functions-handle-the-types-of-parameters-that-you-pass-in


def handle_exception(e: Exception, message: str) -> Union[None, NoReturn]:
    """
    Handles an exception by printing an error message and logging the error.
    The user is prompted to decide whether to reconnect or quit the program.

    Args:
        e (Exception): The exception that occurred.
        message (str): The error message to display.

    Returns:
        None
    """
    print(message)
    print(f"Error details: {e}")
    logging.exception(f"{message} Error details: %s", str(e))
    quitting = input("Do you want to try connecting again? (y/n)\n").lower()
    if quitting == "y":
        print("Reconnecting ...")
        return
    else:
        confirmation = input(
            "Are you sure? If you enter 'y', the program will quit. (y/n)\n"
        ).lower()
        if confirmation == "y":
            print("Quitting due to error.")
            sys.exit(1)
        else:
            print("Reconnecting ...")
            return


# Credit for using the google sheets API:
# https://github.com/Code-Institute-Solutions/love-sandwiches-p5-sourcecode
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


def load_spreadsheet() -> gspread.Spreadsheet:
    """
    Loads the google spreadsheet and sets up the gspread client.

    This function loads the google spreadsheet and sets up the gspread
    client with the required credentials. It uses the 'creds.json'
    file to authenticate the client. It also sets up the gspread client
    with the required scopes. The function also handles exceptions that
    may occur during the setup process.

    Returns:
        gspread.Spreadsheet: The loaded google spreadsheet.
    """
    while True:
        try:
            print("Loading spreadsheet ...")
            CREDS = Credentials.from_service_account_file("creds.json")
            SCOPED_CREDS = CREDS.with_scopes(SCOPE)
            GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
            SPREADSHEET_NAME = "flash_cli_sheet"
            SHEET = GSPREAD_CLIENT.open(SPREADSHEET_NAME)
        except FileNotFoundError as e:
            handle_exception(e, "Failed to load 'creds.json'. Please ensure "
                             "the file exists in the same directory as this "
                             "script.")
        except ValueError as e:
            handle_exception(e, "Failed to load credentials from "
                             "'creds.json'. Please ensure that 'creds.json' "
                             "contains correctly formatted credentials for "
                             "the google API.")
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
            return SHEET


SHEET = load_spreadsheet()

# Credit for writing docstrings:
# https://www.datacamp.com/tutorial/docstrings-python?utm_source=google&utm_medium=paid_search&utm_campaignid=19589720818&utm_adgroupid=157156373751&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=684592138751&utm_targetid=dsa-2218886984100&utm_loc_interest_ms=&utm_loc_physical_ms=9115817&utm_content=&utm_campaign=230119_1-sea~dsa~tofu_2-b2c_3-eu_4-prc_5-na_6-na_7-le_8-pdsh-go_9-na_10-na_11-na&gad_source=1&gclid=CjwKCAiArLyuBhA7EiwA-qo80DbfmFCbaxqMhOuUbjm3RWcqe_zVQXPxO_LL6__tPOFhAhwsABLhxxoCPqwQAvD_BwE


class Flashcard:
    """
    A class to represent a flashcard.

    Attributes:
        question (str): The question on the flashcard.
        answer (str): The answer to the question on the flashcard.
        progress_dict (dict): A dictionary to track the
        progress of the flashcard.

    Methods:
        show_question(): Prints the question on the flashcard.
        show_answer(): Prints the answer to the question on the flashcard.
        update_progress(progress_key: str): Updates the
        progress of the flashcard.

    """

    def __init__(self, question: str, answer: str, progress_dict: dict):
        self.question = question
        self.answer = answer
        self.progress_dict = progress_dict

    def show_question(self) -> None:
        """
        Prints the question on the flashcard.
        """
        print(self.question)

    def show_answer(self) -> None:
        """
        Prints the answer to the question on the flashcard.
        """
        print(self.answer)

    def update_progress(self, progress_key: str) -> None:
        """
        Updates the progress of the flashcard.

        Args:
            progress_key (str): The key to identify the progress to be updated.
        """
        self.progress_dict[progress_key] += 1


class Flashcard_Set:
    """
    A class to represent a set of flashcards.

    Attributes:
        title (str): The title of the flashcard set.
        flashcards (List[Flashcard]): The flashcards in the set.

    Methods:
        _load_flashcards(): Loads the flashcards from the worksheet data.
        show_all(): Displays all the flashcards in a table format.
        upload() -> None: Prepares the flashcard data and uploads it to the
        Google Sheets worksheet.

        Note: The methods above all use helper methods to perform their tasks.
        These helper methods are not listed here.
    """

    def __init__(self, title: str):
        """
        Initializes a Flashcard_Set object.
        Uses the load_flashcards method to load the flashcards from the
        worksheet data.
        """
        self.title = title
        self.flashcards = self._load_flashcards()

    def _load_worksheet_data(self) -> List[Dict[str, Union[int, float, str]]]:
        """
        Loads the worksheet data from Google Sheets.

        Returns:
            List[Dict[str, Union[int, float, str]]]: The worksheet data.
        """
        while True:
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
        """
        Creates a flashcard from a row of data.

        Args:
            row (Dict[str, Union[int, float, str]]): The row of data.

        Returns:
            Flashcard: The created flashcard.
        """
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
        """
        Loads the flashcards from the worksheet data.

        Returns:
            List[Flashcard]: The loaded flashcards.
        """
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
        Converts the flashcards to a list of lists.
        This makes the data compatible with the Google Sheets API.

        Returns:
            list[list]: The flashcards as a list of lists.
        """
        li_of_li = []
        for flashcard in self.flashcards:
            tmp_row = [flashcard.question, flashcard.answer]
            for key in flashcard.progress_dict:
                tmp_row.append(flashcard.progress_dict[key])
            li_of_li.append(tmp_row)
        return li_of_li

    def _prepare_data_for_upload(self) -> list:
        """
        Prepares the flashcard data for upload to Google Sheets.
        - Creates the header row.
        - Converts the flashcards to a list of lists.
        - Prepends the header row to the list of lists.

        Returns:
            list: The prepared data.
        """
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
        """
        Uploads the data to the Google Sheets worksheet.

        Args:
            data (list): The data to upload.
        """
        while True:
            print(f"\nUploading to worksheet: '{self.title}'...")
            try:
                worksheet = SHEET.worksheet(self.title)
                worksheet.clear()
                worksheet.append_rows(data)
            except gspread.exceptions.WorksheetNotFound as e:
                handle_exception(e, f"The worksheet '{
                                 self.title}' was not found.")
            except gspread.exceptions.APIError as e:
                handle_exception(e, "An error occurred with the "
                                 "Google Sheets API.")
            except Exception as e:
                handle_exception(e, "An unexpected error occurred.")
            else:
                print("Successfully uploaded!")
                return

    def upload(self) -> None:
        """
        Prepares the flashcard data and uploads it to the Google Sheets
        worksheet.
        """
        data_to_upload = self._prepare_data_for_upload()
        self._upload_data_to_worksheet(data_to_upload)


def print_worksheet_titles(worksheets: List[gspread.Worksheet]) -> None:
    """
    Prints the titles of the given list of worksheets along with
    an index number for each title.

    Args:
        worksheets (List[gspread.Worksheet]): A list of worksheets.

    Returns:
        None
    """
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
            "\nPlease enter the name of the set you'd like to pick,\nor its "
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
                f"\nor a valid worksheet name."
                "\nTo see the list of Sets again, enter '?'.\n"
            )


def calculate_percentages(card: Flashcard) -> Tuple[int, int, int]:
    """
    Calculates the percentages of correct answers for all quiz types.

    Args:
        card (Flashcard): The flashcard object containing progress information.

    Returns:
        Tuple[int, int, int]: A tuple containing the percentages of correct
            answers of this flashcard for the flashcard quiz, the write quiz,
            and the write quiz with opted correct answers.
    """
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


def generate_feedback_messages(
        feedback: str,
        card: Flashcard
) -> Union[List[str], None]:
    """
    Generate feedback messages based on the given feedback type and flashcard.

    Args:
        feedback (str): The type of requested feedback.
        card (Flashcard): The flashcard object.

    Returns:
        Union[List[str], None]: A list of feedback messages or None if no
        feedback is applicable.

    """
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
    """
    Prints a random feedback message for a given flashcard.

    Args:
        feedback (str): The type of feedback requested.
        card (Flashcard): The flashcard object for which feedback is given.

    Returns:
        None
    """
    message_strings = generate_feedback_messages(feedback, card)
    if message_strings is None:
        return
    rnd_idx = random.randint(0, len(message_strings) - 1)
    print(message_strings[rnd_idx])


def determine_mode(answers: dict) -> str:
    """
    Determines the mode based on the given answers.
    This is to help determine which mode to calculate the accuracy for.

    Args:
        answers (dict): A dictionary containing the answers.

    Returns:
        str: The determined mode. Possible values are "flash_correct"
        or "write_correct".
    """
    if "flash_correct" in answers:
        return "flash_correct"
    else:
        return "write_correct"


def determine_accuracy(set: Flashcard_Set, mode: str, answers: dict) -> int:
    """
    Calculate the accuracy of a flashcard set based on the given mode
    and answers.

    Args:
        set (Flashcard_Set): The flashcard set to calculate accuracy for.
        mode (str): The mode of accuracy calculation. Possible values are
        "flash_correct" and "write_correct".
        answers (dict): A dictionary containing the number of correct answers.

    Returns:
        int: The accuracy percentage rounded to the nearest whole number.
    """
    if mode == "flash_correct":
        return round(answers["flash_correct"] / len(set.flashcards) * 100)
    elif mode == "write_correct":
        return round(
            (answers["write_correct"] + answers["write_correct_user_opted"])
            / len(set.flashcards)
            * 100
        )
    else:
        return 0  # This should never happen


def determine_message_strings(
    set: Flashcard_Set,
    mode: str,
    answers: dict,
    accuracy: int
) -> List[str]:
    """
    Determines the message strings based on the accuracy of the answers.

    Args:
        set (Flashcard_Set): The flashcard set.
        mode (str): The mode of accuracy calculation.
        answers (dict): The correct answers provided by the user.
        accuracy (int): The accuracy of the answers in percentage.

    Returns:
        List[str]: A list of message strings based on the accuracy.

    """
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
    """
    Provides feedback for a given flashcard set based on the user's answers
    After a quiz has been completed.

    Args:
        set (Flashcard_Set): The flashcard set to provide feedback for.
        answers (dict): A dictionary containing the number of correct answers
        for each flashcard.

    Returns:
        None
    """
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
        "In this mode, you'll be shown the question side of each card.\nTry to"
        " answer it in your mind, then press any key to see the answer.\n",
        "i": "Interactive Quiz:\n"
        "In this mode, you'll be shown the question side of each card and "
        "asked to\ntype the answer. Your answer will be checked against the "
        "correct answer.\n",
        "r": "Review All Flashcards:\n"
        "In this mode, you'll see all the questions and answers in the set.\n",
        "c": "Choose a Different Flashcard Set:\n"
        "In this mode, you can go back to the set selection menu to choose a "
        "different\nset of flashcards to study.\n",
    }
    # Credit for join method:
    # https://docs.python.org/3/library/stdtypes.html#str.join
    modes_keys_str = ", ".join(modes.keys())
    back_option_enabled = False

    print("\nMAIN MENU\n")
    print("What would you like to do next?")
    for mode, description in modes.items():
        print(f"{mode}: {description}")
    while True:
        # Credit for case insensitive inputs:
        # https://stackoverflow.com/questions/50192965/how-to-make-user-input-not-case-sensitive
        selected_mode = ""
        if back_option_enabled:
            selected_mode = input(
                f"Select an option ({modes_keys_str}):\n"
                "or 'b' to go back to the main menu.\n"
            ).lower()
        else:
            selected_mode = input(
                f"Select an option ({modes_keys_str}):\n"
            ).lower()
        while True:
            if selected_mode == "b":
                return "b"
            if selected_mode in modes:
                if selected_mode == "?":
                    back_option_enabled = True
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
                    "or 'b' to go back to the main menu.\n"
                ).lower()


def input_or_quit(ipt: str) -> str:
    """
    Function that prompts the user for input and checks if they want to quit.

    Args:
        ipt (str): The prompt message for the user.

    Returns:
        str: The user's input, or 'q' if they choose to quit.
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
        if ipt == "q":
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
    """
    Runs the interactive quiz mode for answering flashcards.

    Args:
        current_set (Flashcard_Set): The flashcard set to be used for the quiz.

    Returns:
        None
    """
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
        if user_answer == "q":
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
                if correction == "q":
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
        if user_answer == "q":
            return
        clear_terminal()
    print("Lesson finished\n")
    give_feedback_set(current_set, answers)
    current_set.upload()
    input("\nPress Enter to go back to the main menu\n")


# Credit to Tim Nelson (CI Mentor) for calling the main function like that.
# https://medium.com/@mycodingmantras/what-does-if-name-main-mean-in-python-fa6b0460a62d#:~:text=The%20if%20__name__,set%20to%20__main__%20.
if __name__ == "__main__":
    """
    This is the main function that controls the flow of the flashcard program.
    It prompts the user to select a mode and then calls the corresponding
    function based on the selected mode.
    """
    print("Welcome to Flashcard CLI!")
    print("This program allows you to practice flashcards and compare your\n"
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
            elif mode == "b":
                continue
