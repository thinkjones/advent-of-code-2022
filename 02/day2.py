
"""
    ROCK        A   X
    PAPER       B   Y
    SCISSORS    C   Z
"""
INPUT_FILE = '02/input.txt'

DECRYPT_RESPONSE = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

WINNER_DICT = {
    "A": "C",   # Rock beats Scissors
    "B": "A",   # Paper beats Rock
    "C": "B"    # Scissors beats Paper
}

LOSER_DICT = {
    "A": "B",   # Rock loses to Paper
    "B": "C",   # Paper loses to Scissors
    "C": "A"    # Scissors loses to Rock
}

SELECTED_SCORE = {
    "A": 1,
    "B": 2,
    "C": 3
}


def fetch_and_decrypt_input(col2_lambda):
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            row = line.rstrip('\n').split(' ')
            row[1] = col2_lambda(row[0], row[1])
            results.append(row)
    return results


def part_two_decrypt(opponent, outcome):
    """ Outcome
        X = Lose
        Y = Draw
        Z = Win
    """

    if outcome == 'Y':
        return opponent
    elif outcome == 'X':
        return WINNER_DICT[opponent]
    elif outcome == 'Z':
        return LOSER_DICT[opponent]


def calculate_score(input):
    total = 0
    for val in input:
        selected_shape_score = SELECTED_SCORE[val[1]]
        win_score = 0
        if val[0] == val[1]:
            win_score = 3
        elif val[0] == WINNER_DICT[val[1]]:
            win_score = 6
        round_score = selected_shape_score + win_score
        total += round_score
    return total


if __name__ == "__main__":
    # Part 1
    print('Day 2 - Part 1')
    col2_lambda = lambda col0, col1: DECRYPT_RESPONSE[col1]
    data = fetch_and_decrypt_input(col2_lambda)
    total_score = calculate_score(data)
    print(total_score)

    # Part 2
    print('Day 2 - Part 2')
    col2_lambda = lambda col0, col1: part_two_decrypt(col0, col1)
    data = fetch_and_decrypt_input(col2_lambda)
    total_score = calculate_score(data)
    print(total_score)

