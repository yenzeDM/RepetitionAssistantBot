class English:
    # add.py
    ADDITION_TEXT_TO_REPEAT = '1️⃣\n\nTo cancel the command, press ⚠️/cancel\n\n✍️Enter any phrase or what you want to repeat.\n\n_"It can be a word, a phrase, a rule that you want to learn. You can add anything you want, it is only limited by your imagination."_:'
    TEXT_TO_REPEAT_HELP_TEXT = '2️⃣\n\n✍️Enter a hint for the previous step that will help you remember what you added.\n\n_"For example, if you added a word in a foreign language in the first step, you should specify the translation in this step."_:'
    HELP_TEXT_DAYS_BEFORE_REPETITION = '3️⃣\n\n✍️ Enter days before repetition from 1️⃣ to 3️⃣0️⃣:'
    DAY_BEFORE_REPETITION_POSITIVE = '✅ You have successfully added new text.'
    DAY_BEFORE_REPETITION_NEGATIVE = '❌ You have specified an incorrect number, please choose a number from 1️⃣ to 3️⃣0️⃣:'
    # add.py, other.py
    MENU = 'Choose any command 🤔'
    # cancel.py
    CANCEL = '✅ Cancellation successful'
    # change_days.py
    CHANGE_HELP_TEXT_ENTER = 'To cancel the command, press ⚠️/cancel\n\n✍️ Please copy and paste the text from the message above _(without the number of days, only the text)_ where you want to change the days until repetition:'
    CHANGE_EMPTY = 'You have nothing in your dictionary 🗑'
    CHANGE_HELP_TEXT_DAYS_BEFORE_REPETITION = '✍️ Enter days before repetition from 1️⃣ to 3️⃣0️⃣:'
    CHANGE_DAYS_POSITIVE = '✅ You have successfully changed days before repetition.'
    CHANGE_DAYS_NEGATIVE_TEXT = '❌ The text is not in your dictionary or you made a mistake, please try again.'
    CHANGE_DAYS_NEGATIVE_NUM = '❌ You have specified an incorrect number, please choose a number from 1️⃣ to 3️⃣0️⃣:'
    # delete.py
    DELETE_TEXT_TYPE_OF_DELETION = 'To cancel the command, press ⚠️/cancel\n\nChoose type of deletion 🫡'
    DELETE_TEXT_EMPTY = 'Your dictionary is empty 🗑'
    DELETE_ALL_POSITIVE = '✅ You deleted all phrases successful'
    DELETE_SEVERAL_TEXT_TO_REPEAT = 'To cancel the command, press ⚠️/cancel\n\n✍Enter several phrases to delete separated by commas.\n\n_(Enter the text that you added in the first step of the "Addition" command.)_:'
    DELETE_ONE_TEXT_TO_REPEAT = 'To cancel the command, press ⚠️/cancel\n\n✍️Enter the text that you want to delete.\n\n_(Enter the text that you added in the first step of the "Addition" command.)_:'
    DELETE_SEVERAL_POSITIVE = '✅ Deletion successful'
    DELETE_SEVERAL_NEGATIVE = '❌ An error occurred, please check if all the phrases are separated by commas and if they are in your dictionary.'
    DELETE_ONE_POSITIVE = '✅ Deletion successful'
    DELETE_ONE_NEGATIVE = '❌ You do not have it in your dictionary or you made a mistake, please try again.'
