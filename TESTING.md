# Testing

Return back to the [README.md](README.md) file.

## Code Validation

### Python

I have used the recommended [PEP8 CI Python Linter](https://pep8ci.herokuapp.com) to validate all of my Python files.

| File | CI URL | Screenshot | Notes |
| --- | --- | --- | --- |
| run.py | [PEP8 CI](https://pep8ci.herokuapp.com/https://raw.githubusercontent.com/benschaf/flash-cli/main/run.py) | ![screenshot](documentation/images/py-validation-run.png) | All clear, no errors found |

Note: The [copy-credits.py](copy-credits.py) file was not validated, as it is a simple script used only for development and not part of the main project.

## Browser Compatibility

I've tested my deployed project on multiple browsers to check for compatibility issues.

| Browser | Screenshot | Notes |
| --- | --- | --- |
| Chrome | ![screenshot](documentation/images/browser-chrome.png) | Works as expected |
| Firefox | ![screenshot](documentation/images/browser-firefox.png) | Works as expected |
| Edge | ![screenshot](documentation/images/browser-edge.png) | Works as expected |
| Opera | ![screenshot](documentation/images/browser-opera.png) | Works as expected |

## Responsiveness

I've tested my deployed project on multiple devices to check for responsiveness issues.

Note: since this is a CLI application, the responsiveness testing is limited. I have still tested on a mobile device and a tablet additionally to the desktop and included the results below.

| Device | Screenshot | Notes |
| --- | --- | --- |
| Google Pixel 6 | ![screenshot](documentation/images/responsive-pixel.png) | Terminal View is too large, inputting commands with the phone keyboard is awkward but it works |
| Desktop | ![screenshot](documentation/images/responsive-desktop.png) | Works as expected, Terminal will only take up top left space of the screen |
| Tablet (emulated) | ![screenshot](documentation/images/responsive-tablet.png) | Works as expected, same inputting issues that are present on mobile |

### Responsiveness within the CLI
The CLI application is not designed to be responsive in the traditional sense, as it is a terminal-based application.
However, lines longer than 80 characters are wrapped manually in the code to ensure that the application is still user friendly when lines are too long for the terminal.

The clear() function is used to clear the terminal screen often, to ensure that the user is not overwhelmed with too much information at once. No scrolling is required, as the terminal is cleared and reprinted with the new information. The information displayed should almost never exceed the height of the terminal.

The exception to the scrolling rule is when the user is reviewing a long deck of flashcards. If the deck is too long, the user will still have to scroll. This is a necessary exception, as the user should be able to review all of their flashcards at once.

## Lighthouse Audit

I've tested my deployed project using the Lighthouse Audit tool to check for any major issues.

| Device | Screenshot | Notes |
| --- | --- | --- |
| Mobile | ![screenshot](documentation/images/lighthouse-mobile.png) | Some minor warnings |
| Desktop | ![screenshot](documentation/images/lighthouse-desktop.png) | Some minor warnings |

The most prominent takeaway from the Lighthouse Audit is that the pageload of the application is affected visibly because the application attempts a download from the Google Sheets API. This is a necessary part of the application, and the user is informed of this while the application is loading.

## Defensive Programming Testing

Defensive programming was manually tested with the below user acceptance testing:

| Checkpoint in Application Flow | Expectation | Test | Result | Fix | Screenshot |
| --- | --- | --- | --- | --- | --- |
| On Application load | A Flashcard Set is expected to be loaded when the user inputs an applicable Number | Tested the feature by inputting Numbers between 1 and 4 | The feature behaved as expected, and loaded each | Test concluded and passed | ![screenshot](documentation/images/defensive-onload-1.gif)
| On Application load | A Flashcard Set is expected to be loaded when the user inputs an applicable String | Tested the feature by inputting Strings | The feature behaved as expected, and loaded each Set | Test concluded and passed | ![screenshot](documentation/images/defensive-onload-2.gif) |
| On Application load | When any other input is given, the user is expected to be prompted to input a valid Number or String | Tested the feature by inputting invalid inputs including out of bound numbers, letters, and symbols | The feature behaved as expected, and prompted the user to input a valid Number or String | Test concluded and passed | ![screenshot](documentation/images/defensive-onload-3.gif) |
| Main Menu | The user is expected to be able to navigate to any of the options in the Main Menu by inputting the applicable letter (case-insensitive) | Tested the feature by inputting the applicable letters | The feature behaved as expected, and navigated to the applicable option | Test concluded and passed | ![screenshot](documentation/images/defensive-mainmenu-1.gif) |
| Main Menu | When any other input is given, the user is expected to be prompted to input a valid letter or to go back to the Main Menu | Tested the feature by inputting invalid inputs including numbers, letters, and symbols and going back to the Main Menu | The feature behaved as expected, and prompted the user to input a valid letter - when 'b' is given as an input the Main Menu is shown again | Test concluded and passed | ![screenshot](documentation/images/defensive-mainmenu-2.gif) |
| Study with Flashcards | The user is expected to be able to reveal the answer to a displayed question by pressing ENTER | Tested the feature by pressing ENTER | The feature behaved as expected, and revealed the answer | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-1.gif) |
| Study with Flashcards | The user is expected to be able to go back to the Main Menu by inputting 'q' after being asked if they are sure to go back | Tested the feature by inputting 'q' | The feature behaved as expected, and went back to the Main Menu after confirming | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-2.gif) |
| Study with Flashcards | When any other input besides from 'q' is given, the input should be ignored and the answer should be shown. | Tested the feature by inputting invalid inputs including numbers, letters, and symbols | The feature behaved as expected, and ignored the input and showed the answer | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-3.gif) |
| Study with Flashcards | After revealing the answer, the user is expected to be able to only input 'y' or 'n' to continue or 'q' to go back to the Main Menu | Tested the feature by inputting 'y', 'n', and 'q' | The feature behaved as expected, and continued, stopped, or went back to the Main Menu | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-4.gif) |
| Study with Flashcards | When any other input besides from 'y', 'n', or 'q' is given, the input should be ignored and the user should be prompted to input a valid letter | Tested the feature by inputting invalid inputs including numbers, letters, and symbols | The feature behaved as expected, and ignored the input and prompted the user to input a valid letter | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-5.gif) |
| Study with Flashcards | Once the user has gone through all the flashcards, the user is expected to be prompted to go back to the Main Menu by pressing ENTER | Tested the feature by pressing ENTER | The feature behaved as expected, and went back to the Main Menu | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-6.gif) |
| Study with Flashcards | When any other input besides from ENTER is given, the input should be ignored and the user should be sent back to the Main Menu | Tested the feature by inputting invalid inputs including numbers, letters, and symbols | The feature behaved as expected, and ignored the input and went back to the Main Menu | Test concluded and passed | ![screenshot](documentation/images/defensive-flashcards-7.gif) |
| Interactive Quiz | The user is expected to be able to answer the question by inputting the correct answer as a string | Tested the feature by inputting the correct answer | The feature behaved as expected, and accepted the correct answer | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-1.gif) |
| Interactive Quiz | If any other input besides the correct answer is given, the answer should be counted as incorrect | Tested the feature by inputting incorrect answers | The feature behaved as expected, and counted the answer as incorrect | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-2.gif) |
| Interactive Quiz | The user is expected to be able to go back to the Main Menu by inputting 'q' after being asked if they are sure to go back | Tested the feature by inputting 'q' | The feature behaved as expected, and went back to the Main Menu after confirming | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-3.gif) |
| Interactive Quiz | After an answer was counted as incorrect, the user should have the option to either treat the answer as correct or incorrect by inputting 'y' or 'n' | Tested the feature by inputting 'y' and 'n' | The feature behaved as expected, and treated the answer as correct or incorrect | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-4.gif) |
| Interactive Quiz | When any other input besides from 'y', 'n', or 'q' is given, the input should be ignored and the user should be prompted to input a valid letter | Tested the feature by inputting invalid inputs including numbers, letters, and symbols | The feature behaved as expected, and ignored the input and prompted the user to input a valid letter | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-5.gif) |
| Interactive Quiz | Once the user has gone through all the questions, the user is expected to be prompted to go back to the Main Menu by pressing ENTER | Tested the feature by pressing ENTER | The feature behaved as expected, and went back to the Main Menu | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-6.gif) |
| Interactive Quiz | When any other input besides from ENTER is given, the input should be ignored and the user should be sent back to the Main Menu | Tested the feature by inputting invalid inputs including numbers, letters, and symbols | The feature behaved as expected, and ignored the input and went back to the Main Menu | Test concluded and passed | ![screenshot](documentation/images/defensive-quiz-6.gif) |
| Review All Flashcards | The user is expected to be able to review all flashcards by scrolling up and down | Tested the feature by scrolling up and down | The feature behaved as expected, and allowed the user to review all flashcards. Note that because of the clear() function bug, the user will sometimes see old content at the top of the terminal | Test concluded, the clear() function bug is known and acceptable | ![screenshot](documentation/images/defensive-review-1.gif) |
| Review All Flashcards | The user is expected to be able to go back to the Main Menu by inputting ENTER, any other input should be ignored | Tested the feature by inputting ENTER and other inputs | The feature behaved as expected, and went back to the Main Menu or ignored the input | Test concluded and passed | ![screenshot](documentation/images/defensive-review-2.gif) |
| Need more details? Just type '?' | The user is expected to be able to either pick one of the menu options or go back to the Main Menu by inputting 'b' | Tested the feature by inputting all menu options and 'b' | The feature behaved as expected, and navigated to the applicable option or went back to the Main Menu | Test concluded and passed | ![screenshot](documentation/images/defensive-details-1.gif) |
| Need more details? Just type '?' | When any other input besides from the menu options or 'b' is given, the user should be prompted to input a valid letter | Tested the feature by inputting invalid inputs including numbers, letters, and symbols | The feature behaved as expected, and prompted the user to input a valid letter | Test concluded and passed | ![screenshot](documentation/images/defensive-details-2.gif) |

## User Story Testing

| User Story | Feature | Screenshot |
| --- | --- | --- |
| As a User, I want to review flashcards in the terminal, so that I can focus on learning without distractions. | Study with Flashcards | ![screenshot](documentation/images/defensive-flashcards-1.gif) |
| As a User, I want to choose between multiple quiz modes, so that I can practice different quiz modes according to my preference and skill level. | Main Menu | ![screenshot](documentation/images/defensive-mainmenu-1.gif) |
| As a User, I want to review a random flashcard and indicate if I knew the definition or not (in flashcard mode), so that I can test my memory of the definition, get immediate feedback, and update the flashcard status. | Study with Flashcards | ![screenshot](documentation/images/defensive-flashcards-4.gif) |
| As a User, I want to see a word and type the definition in typed answer mode, so that I can test my recall and understanding of the definition, get immediate feedback, and update the flashcard status. | Interactive Quiz | ![screenshot](documentation/images/defensive-quiz-1.gif) |
| As an App provider, I want to sync the flashcards with Google Sheets, so that I can easily create and edit flashcard decks online. | Real Time Sync | ![screenshot](documentation/images/defensive-onload-1.gif) |
| As a User, I want to receive real-time feedback based on my performance and the community's performance, so that I can monitor my progress and compare with others. | Real Time Feedback | ![screenshot](documentation/images/feature-feedback.png) |
| As a User, I want to avoid frustration and confusion when an error happens or when I enter invalid input, so that I can have a smooth and enjoyable user experience. | Error Handling and Logging | ![screenshot](documentation/images/feature-error.png) |
| As a User, I want to use keyboard shortcuts and efficient navigation in the terminal, so that I can improve my productivity and user experience. | Whole Application | ![screenshot](documentation/images/feature-main-menu.png) |

## Bugs

I used github Issues to track bugs and fixes. The following bugs were identified and fixed:

[Github Issues labeled as bug](https://github.com/benschaf/flash-cli/issues?q=label%3Abug)

![screenshot](documentation/images/bugs.png)

Note: Some of the bugs were only tracked in github issues retroactively. For these bugs, the commit that fixed the bug is linked in the description of the issue. That way, all of the bugs, fixes and the process of fixing them can be tracked from within Github issues.

## Unfixed Bugs

[When calling review mode multiple times, the first couple of lines repeat (screenshot) #39](https://github.com/benschaf/flash-cli/issues/39)

![screenshot](documentation/images/bug-scroll.png)

- For a full explanation and the history of the bug, see the issue linked above.
- I did not understand this bug for a long time, until my mentor pointed out that the clear() function was not working as expected. It won't clear lines that are not visible anymore because they have been scrolled up too far. This is a known bug and is not fixed, as it is not a priority. The user can still review all flashcards without issue and only a little bit of confusion. -- Thanks [TravelTimN](https://github.com/TravelTimN) for the help with this bug.