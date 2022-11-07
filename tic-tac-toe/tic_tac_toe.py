import json
import copy
from random import randint


def erase_setting():

    setting_names = [
        'set_size', 'set_mode', 'set_symbol_1', 'set_symbol_2',
        'set_difficulty', 'set_name_1', 'set_name_2', 'set_queue', 'set_marks']

    settings = {}

    for item in setting_names:
        settings[item] = 0

    return settings


def game_rate():

    with open('rating.json', 'r', encoding='utf-8') as rating_file:
        rating = json.load(rating_file)

    print('Player Score')

    for k, v in rating.items():
        print(k, v)

    return rating


def game_setting(settings):

    while not (3 <= settings['set_size'] <= 10):
        settings['set_size'] = int(input('Enter battleground size (from 3 (3x3) to 10 (10x10))\n'))
        if not (3 <= settings['set_size'] <= 10):
            print('Try again, make sure your number in range 3-10!')

    while not (settings['set_mode'] in ['m', 's']):
        settings['set_mode'] = input('Choose your destiny! (m - Multi-player, s - Single-player)\n')
        if not (settings['set_mode'] in ['m', 's']):
            print('Try again, make sure your choice equal M or S!')

    while not (settings['set_symbol_1'] in ['X', 'O']):
        settings['set_symbol_1'] = input('Choose first player symbol (X, O)\n')
        if not (settings['set_symbol_1'] in ['X', 'O']):
            print('Try again, make sure your choice equal X or O!')
        if settings['set_symbol_1'] in ['X', 'O']:
            settings['set_symbol_2'] = ['X', 'O']
            settings['set_symbol_2'].remove(settings['set_symbol_1'])
            settings['set_symbol_2'] = ''.join(settings['set_symbol_2'])

    if settings['set_mode'] == 's':
        while not (settings['set_difficulty'] in ['e', 'h']):
            settings['set_difficulty'] = input('Choose AI difficulty (e - Easy, h - Hard)\n')
            if not (settings['set_difficulty'] in ['e', 'h']):
                print('Try again, make sure your choice equal e or h!')
        if settings['set_difficulty'] == 'e':
            settings['set_name_1'] = input('Enter player name:\n')
            settings['set_name_2'] = 'Yorick'
        else:
            settings['set_name_1'] = input('Enter player name:\n')
            settings['set_name_2'] = 'Herald'

    if settings['set_mode'] == 'm':
        settings['set_name_1'] = input('Enter first player name:\n')
        settings['set_name_2'] = input('Enter second player name:\n')

    while not (settings['set_queue'] in [1, 2]):
        settings['set_queue'] = int(input('Enter whose first turn (Player 1 - 1, Player 2 (AI) - 2)\n'))
        if not (settings['set_queue'] in [1, 2]):
            print('Try again, make sure you enter 1 or 2!')

    if settings['set_size'] in [3, 4]:
        settings['set_marks'] = 3
    if settings['set_size'] in [5, 6]:
        settings['set_marks'] = 4
    if settings['set_size'] in [7, 8, 9, 10]:
        settings['set_marks'] = 5

    settings['set_size'] += 1

    return settings


def game_start(settings):

    field = list(range(settings['set_size']))
    for i in range(settings['set_size']):
        field[i] = list(range(settings['set_size']))

    for i in range(settings['set_size']):
        for j in range(settings['set_size']):
            if i == 0 and j == 0:
                field[i][j] = ' '
            elif i == 0:
                field[i][j] = j
            elif j == 0:
                field[i][j] = i
            else:
                field[i][j] = '-'

    print('Play session has been set up and ready for play! GL HF!')

    for row in field:
        print(*row)

    return field


def game_end(settings, game_result, counter):

    global wanna_leave
    global save_setting

    wanna_leave = ''
    save_setting = ''
    player_1_name = settings['set_name_1']
    player_2_name = settings['set_name_2']
    queue = settings['set_queue']

    if game_result == 'Win!':
        print(
            f'Congratulations! '
            f'{player_1_name if (counter + queue) % 2 == 0 else player_2_name} has won! He gets 10 points!')
    if game_result == 'Draw!':
        print('Unfortunately it\'s draw! The important thing is not to win but to take part!')
    while wanna_leave not in ['y', 'n']:
        wanna_leave = input('Are you willing to end game session? (y/n)\n')
        if wanna_leave not in ['y', 'n']:
            print('Try again, make sure your choice equal y or n!')
    if wanna_leave == 'n':
        while save_setting not in ['y', 'n']:
            save_setting = input('Are you willing to use previous settings? (y/n)\n')
            if save_setting not in ['y', 'n']:
                print('Try again, make sure your choice equal y or n!')


def field_update(settings, field, turn_result, counter):

    if (counter + settings['set_queue']) % 2 == 0:
        actual_turn_player_symbol = settings['set_symbol_1']
    else:
        actual_turn_player_symbol = settings['set_symbol_2']

    if not(turn_result != 'Win!' or turn_result != 'Draw!'):
        field[turn_result[0]][turn_result[1]] = actual_turn_player_symbol

    for row in field:
        print(*row)

    return field


def player_turn(settings, field, counter, rating):

    def check_empty(field_check, player_decision):

        check_empty_sign = 0

        if 1 <= player_decision[0] < len(field_check) and 1 <= player_decision[1] < len(field_check):
            if field_check[player_decision[0]][player_decision[1]] != '-':
                print('This cell already busy! Try again!')
            else:
                check_empty_sign = 1

        return check_empty_sign

    def check_limits(player_decision, field_size):

        if not (
                (1 <= player_decision[0] < field_size['set_size'])
                and (1 <= player_decision[1] < field_size['set_size'])):
            print('This cell is out of battlefield! Try again!')
            check_limits_sign = 0
        else:
            check_limits_sign = 1

        return check_limits_sign

    def check_win(field_check, player_name, player_decision, player_symbol, sets, player_rating):

        field_check[player_decision[0]][player_decision[1]] = player_symbol
        check_diagonal_tor = 0
        check_diagonal_tol = 0
        check_row = 0
        check_col = 0
        temp_count = 0
        win_check_result = ''

        for row in field_check:
            for element in row:
                if element == 'X' or element == 'O':
                    temp_count += 1

        for i in range(player_decision[0] - sets['set_marks'] + 1, player_decision[0] + sets['set_marks']):
            for j in range(player_decision[1] - sets['set_marks'] + 1, player_decision[1] + sets['set_marks']):
                if ((i == j + player_decision[0] - player_decision[1]) and (1 <= i < sets['set_size'])
                        and (1 <= j < sets['set_size']) and (field_check[i][j] == player_symbol)):
                    check_diagonal_tor += 1
                if ((i + j == player_decision[0] + player_decision[1]) and (1 <= i < sets['set_size'])
                        and (1 <= j < sets['set_size']) and (field_check[i][j] == player_symbol)):
                    check_diagonal_tol += 1
                if (i == player_decision[0]) and (1 <= j < sets['set_size']) and (field_check[i][j] == player_symbol):
                    check_row += 1
                if (j == player_decision[1]) and (1 <= i < sets['set_size']) and (field_check[i][j] == player_symbol):
                    check_col += 1

        check_diagonal_tor = True if check_diagonal_tor == sets['set_marks'] else False
        check_diagonal_tol = True if check_diagonal_tol == sets['set_marks'] else False
        check_row = True if check_row == sets['set_marks'] else False
        check_col = True if check_col == sets['set_marks'] else False

        if check_diagonal_tor or check_diagonal_tol or check_col or check_row:
            win_check_result = 'Win!'
            winner_name = player_name
            winner_rate = 10
            player_rating[winner_name] += winner_rate
            with open('rating.json', 'w') as rating_file:
                rating_file.write(json.dumps(game_rating))

        if (temp_count == (sets['set_size'] - 1) ** 2) and (win_check_result != 'Win!'):
            win_check_result = 'Draw!'

        return win_check_result

    def easy_drive(easy_field, sets):

        player_decision = [0, 0]

        while easy_field[player_decision[0]][player_decision[1]] != '-':
            player_decision = [randint(1, sets['set_size']-1), randint(1, sets['set_size']-1)]

        return player_decision

    def hard_drive(field_check, actual_player_symbol, sets):

        def hard_checks(fck, my_mark, enemy_mark, sets_1):

            fck_weights = copy.deepcopy(fck)
            for i_1 in range(len(fck_weights)):
                for j_1 in range(len(fck_weights)):
                    fck_weights[i_1][j_1] = 0

            nn = len(fck)

            for i_1 in range(1, nn):
                for j_1 in range(1, nn):

                    main_d_check_en = 0
                    sec_d_check_en = 0
                    row_check_en = 0
                    col_check_en = 0
                    main_d_check_my = 0
                    sec_d_check_my = 0
                    row_check_my = 0
                    col_check_my = 0

                    if fck[i_1][j_1] == enemy_mark:

                        for i_2 in range(i_1 - sets_1['set_marks'] + 1, i_1 + sets_1['set_marks']):
                            for j_2 in range(j_1 - sets_1['set_marks'] + 1, j_1 + sets_1['set_marks']):
                                if ((i_2 == j_2 + i_1 - j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn)
                                        and fck[i_2][j_2] == enemy_mark):
                                    main_d_check_en += 1
                                if ((i_2 + j_2 == i_1 + j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn)
                                        and fck[i_2][j_2] == enemy_mark):
                                    sec_d_check_en += 1
                                if (i_2 == i_1) and (1 <= j_2 < nn) and fck[i_2][j_2] == enemy_mark:
                                    row_check_en += 1
                                if (j_2 == j_1) and (1 <= i_2 < nn) and fck[i_2][j_2] == enemy_mark:
                                    col_check_en += 1

                        for i_2 in range(i_1 - sets_1['set_marks'] + 1, i_1 + sets_1['set_marks']):
                            for j_2 in range(j_1 - sets_1['set_marks'] + 1, j_1 + sets_1['set_marks']):
                                if (i_2 == j_2 + i_1 - j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn) and (
                                        main_d_check_en >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4):
                                    fck_weights[i_2][j_2] += 2
                                if (i_2 + j_2 == i_1 + j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn) and (
                                        sec_d_check_en >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4):
                                    fck_weights[i_2][j_2] += 2
                                if ((i_2 == i_1) and (1 <= j_2 < nn)
                                        and (row_check_en >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4)):
                                    fck_weights[i_2][j_2] += 2
                                if ((j_2 == j_1) and (1 <= i_2 < nn)
                                        and (col_check_en >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4)):
                                    fck_weights[i_2][j_2] += 2

                    if fck[i_1][j_1] == my_mark:

                        for i_2 in range(i_1 - sets_1['set_marks'] + 1, i_1 + sets_1['set_marks']):
                            for j_2 in range(j_1 - sets_1['set_marks'] + 1, j_1 + sets_1['set_marks']):
                                if (i_2 == j_2 + i_1 - j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn):
                                    fck_weights[i_2][j_2] += 1
                                if (i_2 + j_2 == i_1 + j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn):
                                    fck_weights[i_2][j_2] += 1
                                if (i_2 == i_1) and (1 <= j_2 < nn):
                                    fck_weights[i_2][j_2] += 1
                                if (j_2 == j_1) and (1 <= i_2 < nn):
                                    fck_weights[i_2][j_2] += 1

                        for i_2 in range(i_1 - sets_1['set_marks'] + 1, i_1 + sets_1['set_marks']):
                            for j_2 in range(j_1 - sets_1['set_marks'] + 1, j_1 + sets_1['set_marks']):
                                if ((i_2 == j_2 + i_1 - j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn)
                                        and fck[i_2][j_2] == my_mark):
                                    main_d_check_my += 1
                                if ((i_2 + j_2 == i_1 + j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn)
                                        and fck[i_2][j_2] == my_mark):
                                    sec_d_check_my += 1
                                if (i_2 == i_1) and (1 <= j_2 < nn) and fck[i_2][j_2] == my_mark:
                                    row_check_my += 1
                                if (j_2 == j_1) and (1 <= i_2 < nn) and fck[i_2][j_2] == my_mark:
                                    col_check_my += 1

                        for i_2 in range(i_1 - sets_1['set_marks'] + 1, i_1 + sets_1['set_marks']):
                            for j_2 in range(j_1 - sets_1['set_marks'] + 1, j_1 + sets_1['set_marks']):
                                if (i_2 == j_2 + i_1 - j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn) and (
                                        main_d_check_my >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4):
                                    fck_weights[i_2][j_2] += 2
                                if (i_2 + j_2 == i_1 + j_1) and (1 <= i_2 < nn) and (1 <= j_2 < nn) and (
                                        sec_d_check_my >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4):
                                    fck_weights[i_2][j_2] += 2
                                if ((i_2 == i_1) and (1 <= j_2 < nn)
                                        and (row_check_my >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4)):
                                    fck_weights[i_2][j_2] += 2
                                if ((j_2 == j_1) and (1 <= i_2 < nn)
                                        and (col_check_my >= sets_1['set_marks'] - 1 - sets_1['set_marks'] // 4)):
                                    fck_weights[i_2][j_2] += 2

            for i_1 in range(1, nn):
                for j_1 in range(1, nn):
                    if fck[i_1][j_1] == enemy_mark or fck[i_1][j_1] == my_mark:
                        fck_weights[i_1][j_1] = 0

            return fck_weights

        enemy_symbol = ['X', 'O']
        enemy_symbol.remove(actual_turn_player_symbol)
        enemy_symbol = ''.join(enemy_symbol)
        field_weights = hard_checks(field_check, actual_player_symbol, enemy_symbol, sets)
        maxim = max(map(max, field_weights))
        maxim_index_row = []
        maxim_index_col = []

        for i in range(len(field_weights)):
            for j in range(len(field_weights)):
                if field_weights[i][j] == maxim:
                    maxim_index_row.append(i)
                    maxim_index_col.append(j)

        maxim_index_base = list(zip(maxim_index_row, maxim_index_col))
        maxim_index = []

        for row in maxim_index_base:
            if 0 not in row:
                maxim_index.append(row)

        randomize_my_turn = randint(0, len(maxim_index)-1)
        my_turn_decision = [maxim_index[randomize_my_turn][0], maxim_index[randomize_my_turn][1]]
        print('weight_table')
        for row in field_weights:
            print(*row)
        print(f'maxim = {maxim}')
        print(f'maxim_index= {maxim_index}')
        print(f'randomize_my_turn = {randomize_my_turn}')
        print(f'my_turn_decision = {my_turn_decision}')

        return my_turn_decision

    check_empty_ok = 0
    check_limits_ok = 0
    actual_turn_player_decision = ''

    if (counter + settings['set_queue']) % 2 == 0:
        actual_turn_player_name = settings['set_name_1']
        actual_turn_player_symbol = settings['set_symbol_1']
    else:
        actual_turn_player_name = settings['set_name_2']
        actual_turn_player_symbol = settings['set_symbol_2']

    print(f'Turn number {counter}! \nPlayer {actual_turn_player_name} turn with {actual_turn_player_symbol}!')

    if settings['set_mode'] == 'm' \
            or (settings['set_mode'] == 's' and actual_turn_player_name == settings['set_name_1']):
        while (check_empty_ok == 0) or (check_limits_ok == 0):
            n = input(f'Enter the cell index (separated by space) to put {actual_turn_player_symbol}\n')
            actual_turn_player_decision = [int(x) for x in n.split()]
            check_limits_ok = check_limits(actual_turn_player_decision, settings)
            check_empty_ok = check_empty(field, actual_turn_player_decision)

    if settings['set_mode'] == 's' \
            and settings['set_difficulty'] == 'e' \
            and actual_turn_player_name == settings['set_name_2']:
        actual_turn_player_decision = easy_drive(field, settings)

    if settings['set_mode'] == 's' \
            and settings['set_difficulty'] == 'h' \
            and actual_turn_player_name == settings['set_name_2']:
        actual_turn_player_decision = hard_drive(field, actual_turn_player_symbol, settings)

    result_condition = check_win(
        field, actual_turn_player_name, actual_turn_player_decision,
        actual_turn_player_symbol, settings, rating)

    if result_condition in ['Win!', 'Draw!']:
        turn_result = result_condition
    else:
        turn_result = actual_turn_player_decision

    return turn_result


wanna_leave = 'n'
save_setting = 'n'
game_settings_chart = {}

while wanna_leave == 'n':

    if save_setting == 'n':
        game_settings_chart = erase_setting()
        game_settings_chart = game_setting(game_settings_chart)

    player_turn_result = ''
    turn_counter = 0
    game_rating = game_rate()
    battlefield = game_start(game_settings_chart)

    while player_turn_result not in ['Win!', 'Draw!']:
        turn_counter += 1
        player_turn_result = player_turn(game_settings_chart, battlefield, turn_counter, game_rating)
        battlefield = field_update(game_settings_chart, battlefield, player_turn_result, turn_counter)

    game_end(game_settings_chart, player_turn_result, turn_counter)
