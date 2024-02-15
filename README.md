# Flash-CLI: Command-Line Vocabulary Training

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Flash-CLI is a Python-based command-line vocabulary training application that seamlessly integrates with Google Sheets. Enhance your language skills, track progress, and master new words—all from your terminal.

## UX

### User Stories

### Flowchart

### Why the Terminal?
The terminal is an ideal environment for vocabulary training for several reasons:

- **Focus on Learning:** By removing distractions (fancy UI elements, animations, etc.), the terminal allows users to concentrate solely on expanding their vocabulary.
- **Efficiency:** Terminal apps are lightweight and fast. Users can quickly launch the app, practice, and exit, thereby maximizing their time spent learning. 
- **Keyboard-Centric Interaction:** Terminal apps encourage keyboard shortcuts and efficient navigation, which aligns well with learning and memorization.

_Note_: For this specific project, the terminal environment is emulated within a browser. However, the app is designed to be used in a traditional terminal environment.

## Features

### Quiz Mode
Test your vocabulary knowledge interactively.
- Answer flashcard questions.
- Difficulty adjusts based on your progress.
- Chose from multiple-choice or fill-in-the-blank questions.

### Adding New Flashcards
Add new words and definitions to your vocabulary list.
- Use the app to add new words and definitions.
- Google Sheets reflects these changes.

### Learning Progress
Monitor the progress of all of your flashcards.
- Each flashcard's progress is stored.
- Update the Google Sheets document accordingly.

### Real-Time Google Sheets Sync
Automatically update your vocabulary data in a connected Google Sheets document.

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
