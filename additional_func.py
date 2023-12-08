import datetime


async def handler_for_show_list(list, phrase=None, translation=None, date=None, days=None):
    result = []
    output_values = {
        'phrase': phrase,
        'translation': translation,
        'date': date,
        'days': days,
    }
    index = [3, 2, 1, 0]

    for i in output_values.copy():
        if output_values[i]:
            output_values[i] = index[-1]
            index.pop()
        else:
            output_values.pop(i)
            index.pop()
    amount = len(output_values)
    output_number = ''
    for i in range(amount):
        output_number += '{' + f'{i}' + '} - '
    for i in list:
        result.append(output_number.strip(' - ').format(*
                      [i[j] for j in output_values.values()]))
    return '\n\n'.join(result)


async def phrases_to_repeat(all_user_phrases):
    result = []
    todays_date = datetime.datetime.strptime(
        str(datetime.date.today()), '%Y-%m-%d')
    # сортирует по дням до повторения все слова юзера
    for i, j, date, days_before_repetition in sorted(all_user_phrases, key=lambda list: list[3]):
        date_of_addition = datetime.datetime.strptime(date, '%Y-%m-%d')
        days_gone_by = todays_date - date_of_addition
        if days_gone_by.days < days_before_repetition:
            continue
        else:
            result.append((i, j, date, days_before_repetition))
    return result
