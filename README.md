# Flash-CLI: Command-Line Vocabulary Training

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Flash-CLI is a Python-based command-line vocabulary training application that seamlessly integrates with Google Sheets. Enhance your language skills, track progress, and master new words—all from your terminal.

## UX

### User Stories

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
#### Flashcard Mode: Users can review flashcards and decide if they know the answer.
Functionality:
- Display a random flashcard only with the word (question).
- Upon user input, reveal the definition (answer).
- Prompt the user to indicate if they knew the answer or not.
- Update the flashcard status based on the user's response.
This mode is designed to help users for initial learning and self-assessment of their vocabulary. It's a simple and effective way to memorize new words and their meanings.
#### Typed Answer Quizzes: Users type their answers directly.
Functionality:
- Display a word (question).
- Prompt the user to type the definition (answer).
- Check the user's input against the correct definition.
- If the user's input is incorrect, display the correct definition and ask the user if they want to count their attempt as a success or failure.
- Update the flashcard status based on the user's responses.
This mode is designed to test the user's recall and understanding of the vocabulary. It's a more challenging and interactive way to practice and reinforce learning.

### Real-Time Google Sheets Sync
The app automatically syncs vocabulary data with a connected Google Sheets document. This feature allows users to:
- Add new words and definitions directly to the Google Sheets document.
- Update existing flashcards with new information.
- Export flashcards from google sheets to third-party applications.
- Import flashcards from third-party applications to google sheets.

The Google Sheet is set up so that every worksheet is a deck of flashcards. Each row represents a flashcard, with the word in the first column and the definition in the second column. The third column is used to store the status of the flashcard (1-5).

### Error Handling and Logging
Flash-CLI gracefully handles unexpected errors and provides helpful messages to guide users. Additionally, the app logs application events for debugging and troubleshooting.

#### Gracefully handle unexpected errors (e.g., invalid input, network issues).
Invalid input: If the user enters an invalid command or input, the app will display a helpful message and prompt the user to try again.

## Future Features

### Quiz Modes
- Multiple-Choice Quizzes: Randomized questions with answer choices.
- Timed Quizzes: Set a time limit for answering questions.

### Flashcard Management
- Create, edit, and delete flashcards.
- Tag flashcards for better categorization.
- Organize flashcards into decks or collections.

### Spaced Repetition
- Implement a spaced repetition algorithm (e.g., Leitner system) to optimize learning intervals.
- Gradually increase intervals for well-remembered words.
- Remind users to review flashcards at optimal times.

### Statistics and Analytics
- Display overall progress (e.g., percentage of mastered words).
- Show performance trends over time (graphs, charts).
- Identify areas where improvement is needed (e.g., low success rate on specific flashcards).

### Interactive Help System
- Provide built-in documentation accessible via commands (e.g., help, man).
- Explain features, usage, and available commands.

### Import/Export
- Import: Allow users to import existing vocabulary lists from other sources (e.g., Quizlet, Anki).
    - Just the import from quizlet would be an amazing ap in itself because exporting from quizlet to a spreadsheet is a pain.
- Export: Enable users to export flashcards (e.g., as CSV files) for sharing or backup.

### Integration with Language APIs
#### Use language APIs (e.g., WordNet, Google Translate) for:
- Synonyms and antonyms
- Example sentences
- Word definitions
- Pronunciations

### Gamification
- Points and Badges: Reward users with points for completing quizzes or achieving milestones.
- Daily Streaks: Encourage consistent practice by maintaining daily streaks.

### Customizable Themes
- Allow users to choose color schemes for the terminal interface (e.g., light mode, dark mode).
- Use the rich library to create a more visually appealing interface.

### Backup and Restore
#### Regularly back up user data (flashcards, progress) to prevent data loss.
- Provide an option to restore from backups if needed (e.g., after reinstalling the app).

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
