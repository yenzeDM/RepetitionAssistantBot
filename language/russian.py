class Russian:
    # add.py
    ADD_TEXT_TO_REPEAT = '1️⃣\n\nДля отмены команды нажмите ⚠️/cancel\n\n✍️ Введите любую фразу или то, что хотите повторить.\n\n_"Это может быть слово, фраза, правило, которое вы хотите выучить. Добавить можно все что угодно, это ограничивается только вашим воображением."_:'
    ADD_HELP_TEXT = '2️⃣\n\n✍️ Введите подсказку для предыдущего шага, которая сможет помочь вам вспомнить что вы добавляли.\n\n_"Например, если в первом шаге вы добавляли слово на иностранном языке, то в этом шаге нужно указать перевод."_:'
    ADD_DAYS_BEFORE_REPETITION = '3️⃣\n\n✍️ Введите количество дней до повторения от 1️⃣ до 3️⃣0️⃣:'
    ADD_POSITIVE = '✅ Вы успешно добавили текст'
    ADD_NEGATIVE = '❌ Вы указали неправильное количество дней, пожалуйста, укажите от 1️⃣ до 3️⃣0️⃣:'
    # add.py, other.py
    KEYBOARD_WITH_COMMANDS = 'Выберите команду 🤔'
    # cancel.py
    CANCEL = '✅ Вы успешно отменили действие'
    # change_days.py
    CHANGE_HELP_TEXT = '1️⃣\n\nДля отмены команды нажмите ⚠️/cancel\n\n✍️ Скопируйте и вставьте текст из сообщения выше _(Без количества дней только текст)_, где вы хотите поменять дни до повторения:'
    CHANGE_EMPTY = 'Ваш словарь пустой 🗑'
    CHANGE_DAYS_BEFORE_REPETITION = '2️⃣\n\n✍️ Введите количество дней до повторения от 1️⃣ до 3️⃣0️⃣:'
    CHANGE_POSITIVE = '✅ Вы успешно поменяли количество дней.'
    CHANGE_NEGATIVE_TEXT = '❌ Текста нет в вашем словаре или вы допустили ошибку, попробуйте еще раз.'
    CHANGE_NEGATIVE_NUM = '❌ Это число не доступно, пожалуйста, укажите от 1️⃣ до 3️⃣0️⃣:'
    # delete.py
    DELETE_TEXT_TYPE_OF_DELETION = 'Для отмены команды нажмите ⚠️/cancel\n\nChoose type of deletion 🫡'
    DELETE_TEXT_EMPTY = 'Ваш словарь пустой 🗑'
    DELETE_ALL_POSITIVE = '✅ Вы успешно удалили весь текст'
    DELETE_SEVERAL_TEXT_TO_REPEAT = 'Для отмены команды нажмите ⚠️/cancel\n\n✍ Для удаления введите несколько фраз через запятую.\n\n_"Введите текст, который вы добавляли в первом шаге команды Addition"_:'
    DELETE_ONE_TEXT_TO_REPEAT = 'Для отмены команды нажмите ⚠️/cancel\n\n✍️ Введите текст который хотите удалить.\n\n_"Введите текст, который вы добавляли в первом шаге команды Addition"_:'
    DELETE_SEVERAL_POSITIVE = '✅ Вы успешно удалили текст'
    DELETE_SEVERAL_NEGATIVE = '❌ Текста нет в вашем словаре, пожалуйста, проверьте все ли фразы разделены запятой и находяться ли они в вашем словаре.'
    DELETE_ONE_POSITIVE = '✅ Вы успешно удалили текст'
    DELETE_ONE_NEGATIVE = '❌ Текста нет в вашем словаре или вы допустили ошибку, попробуйте еще раз.'
    # learn.py
    LEARN_NEED = 'Для отмены команды нажмите ⚠️/cancel\n\n🧾 Сегодня нужно повторить:'
    LEARN_EMPTY = 'У вас нет слов для повторения 🗑'
    LEARN_TEXT_TO_REPEAT = '✍️ Введите ответ:'
    FINISH_LEARN_TEXT_TO_REPEAT = "На сегодня все 👏"
    LEARN_TEXT_TO_REPEAT_POSITIVE = '✅ Правельный ответ'
    LEARN_TEXT_TO_REPEAT_NEGATIVE = '❌ Неправильный ответ'
    # other.py
    START = '''👋 Привет, я твой <b>помощник для повторения</b>.

Введите команду /keyboard_with_commands для добавления и изучения вашего материала.

Используйте команду /help для ознакомления со <b>всеми командами</b> и <b>их подробным описанием</b>.'''
    HELP = '''🔻 /start - начать работу с ботом.
🔸 /help - описание команд.
🔹 /keyboard_with_commands - клавиатура с основными командами.
▫️ /cancel - отмена действия.

<b>Описание основных команда:</b>

📓 <b>Learning</b> - команда для изучения добавленого материала. Вы можете вызвать эту команду написав <b>"Learning"</b> в чат с ботом.

🧾 <b>List of phrases</b> - показывает весь добавленый материал. Вы можете вызвать эту команду написав <b>"List"</b> в чат с ботом.

🎲 <b>Change days before repetition</b> - меняет дни до повторения. Вы можете вызвать эту написав <b>"Change"</b> в чат с ботом.

📨 <b>Addition</b> - добавляет материал в ваш словарь. Вы можете вызвать эту команду написав <b>"Addition"</b> в чат с ботом.

✂️ <b>Deletion</b> - удаляет материал из вашего словаря. Вы можете вызвать эту команду написав <b>"Deletion"</b> в чат с ботом.'''
    LIST_EMPTY = 'Ваш словарь пустой 🗑'
