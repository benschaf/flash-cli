# Flash-CLI: Command-Line Vocabulary Training

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Flash-CLI is a Python-based command-line flashcard application that seamlessly integrates with Google Sheets. Enhance your skills, compare your progress with everyone who used the app before, and master all kinds of flashcards — all from a Command Line Interface.

[Link to google Spreadsheet](https://docs.google.com/spreadsheets/d/1hGXKTWDj8vrl2kdby4OqQysjKpAUj-r4rwd_002I7Vc/edit?usp=sharing)

[Link to live Website](https://flash-cli-1471beedfcc0.herokuapp.com/)

## UX

### User Stories
| As a | I want to | so that I can |
| --- | --- | --- |
| User | review flashcards in the terminal | focus on learning without distractions |
| User | choose between multiple quiz modes | practice different quiz modes according to my preference and skill level |
| User | review a random flashcard and indicate if I knew the definition or not (in flashcard mode) | test my memory of the definition, get immediate feedback, and update the flashcard status |
| User | see a word and type the definition in typed answer mode | test my recall and understanding of the definition, get immediate feedback, and update the flashcard status |
| App provider | sync the flashcards with Google Sheets | easily create and edit flashcard decks online |
| User | receive real-time feedback based on my performance and the community's performance | monitor my progress and compare with others |
| Developer | handle errors gracefully and provide helpful messages | avoid frustration and confusion for users of the app |
| User | use keyboard shortcuts and efficient navigation in the terminal | improve my productivity and user experience |

### Flowchart
Link to the [Flowchart](https://drive.google.com/file/d/1rDfChnROSVD_QkKvOzWtL8e4Z6Wk0UX-/view?usp=sharing)

### Why the Terminal?
The terminal is an ideal environment for vocabulary training for several reasons:

- **Focus on Learning:** By removing distractions (fancy UI elements, animations, etc.), the terminal allows users to concentrate solely on expanding their vocabulary.
- **Efficiency:** Terminal apps are lightweight and fast. Users can quickly launch the app, practice, and exit, thereby maximizing their time spent learning.
- **Keyboard-Centric Interaction:** Terminal apps encourage keyboard shortcuts and efficient navigation, which aligns well with learning and memorization.

_Note_: For this specific project, the terminal environment is emulated within a browser. However, the app is designed to be used in a traditional terminal environment.

## Features

### Quiz Modes

#### Main Menu and Navigation
The app provides a main menu with options to choose between different quiz modes and to exit the app. Users can navigate the app using keyboard shortcuts that are displayed in the menu. If the user wishes to have more information about the options, they can use the help (?) command.
All invalid inputs are handled gracefully, and the app provides helpful messages to guide users.
![Main Menu](docs/images/feature-main-menu.png)

#### Flashcard Mode: Users can review flashcards and decide if they know the answer.
Functionality:
- Display a random flashcard only with the word (question).
- Upon user input, reveal the definition (answer).
- Prompt the user to indicate if they knew the answer or not.
- Update the flashcard status based on the user's response.
- Provide personalized feedback based on the user's responses and the responses of the community so far.
This mode is designed to help users for initial learning and self-assessment. It's a simple and effective way to memorize new flashcards.
![Flashcard Mode](docs/images/feature-flashcard-mode.png)

#### Typed Answer Quizzes: Users type their answers directly.
Functionality:
- Display a word (question).
- Prompt the user to type the definition (answer).
- Check the user's input against the correct definition.
- If the user's input is incorrect, display the correct definition and ask the user if they want to count their attempt as a success or failure.
- Update the flashcard status based on the user's responses.
- Provide personalized feedback based on the user's responses and the responses of the community so far.
This mode is designed to test the user's recall and understanding of the flashcard. It's a more challenging and interactive way to practice and reinforce learning.
![Typed Answer Mode](docs/images/feature-typed-answer-mode.png)

### Real-Time Google Sheets Sync
The app automatically syncs flashcard data with a connected Google Sheets document using the Google Sheets API. No user login is required.

The Google Sheet is set up so that every worksheet is a deck of flashcards. Each row represents a flashcard, with the word in the first column and the definition in the second column. Further columns are used to store the status of the flashcard.
![Google Sheets](docs/images/feature-google-sheets-sync.png)

### Real-Time Feedback:
The app will provide personalized and dynamically generated feedback based on collective performance. Feedback is given after answering most questions and at the end of each quiz. It's designed to motivate users and help put their progress into perspective.

Here are some examples of the feedback:
- "Great job! You're part of the 70% of people who knew the answer!"
- "You're doing better than 30% of people who attempted this flashcard."
- "You knew the answer! Great job!"
- "Don't worry, less than half of the people who attempted this flashcard knew the answer."
- "You're doing better than 40% of people who attempted this flashcard."
- "You wrote the correct answer! Great job!"
- "You're doing better than 20% of people who attempted this flashcard."
- "50% of people opted to treat the answer as correct or wrote it correctly. Keep practicing!"

### Error Handling and Logging
Flash-CLI gracefully handles unexpected errors and provides helpful messages to guide users. Additionally, the app logs application events for debugging and troubleshooting.

This is achieved using a custom built helper function:
```python
def handle_exception(e: Exception, message: str) -> NoReturn:
    """
    Handles an exception by printing an error message, logging the error,
    and exiting the program.

    Args:
        e (Exception): The exception that occurred.
        message (str): The error message to display.

    Returns:
        None
    """
    print(message)
    print(f"Error details: {e}")
    logging.exception(f"{message} Error details: %s", str(e))
    print("Quitting due to error.")
    sys.exit(1)
```
[View Code in project](https://github.com/benschaf/flash-cli/blob/04f1b1e25fe9bb4242dcb49575435691b4b7cfb1/run.py#L58-L74)

An example of how this function is called:
```python
try:
    # more code ...
    CREDS = Credentials.from_service_account_file("creds.json")
    # more code ...
except FileNotFoundError as e:
    handle_exception(e, "Failed to load 'creds.json'. Please ensure the file "
                     "exists in the same directory as this script.")
```
[Vew code in project](https://github.com/benschaf/flash-cli/blob/04f1b1e25fe9bb4242dcb49575435691b4b7cfb1/run.py#L77-L86)

#### Gracefully handle unexpected errors (e.g., invalid input, network issues).
Invalid input: If the user enters an invalid command or input, the app will display a helpful message and prompt the user to try again.

Example:
![Invalid Input](docs/images/feature-invalid-input.png)

## Future Features

### Quiz Modes
- Multiple-Choice Quizzes: Randomized questions with answer choices.
- Timed Quizzes: Set a time limit for answering questions.

### Flashcard Management
- Create, edit, and delete flashcard decks.

### Statistics and Analytics
- Display global progress (e.g., percentage of how many people knew an answer).
- Show performance trends over time (graphs, charts).

### Integration with Language APIs
#### Use language APIs (e.g., WordNet, Google Translate) for:
- Synonyms and antonyms
- Example sentences
- Word definitions
- Pronunciations

### Gamification
- Points and Badges: Reward users with points for completing quizzes or achieving milestones.

### Customizable Themes
- Allow users to choose color schemes for the terminal interface (e.g., light mode, dark mode).
- Use the rich library to create a more visually appealing interface.

### Backup and Restore
#### Regularly back up user data (flashcards, progress) to prevent data loss.

### Tools

- [Google Sheets API](https://developers.google.com/sheets/api)
- [Quizlet](https://quizlet.com/)

## Credits





![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **March 14, 2023**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!
