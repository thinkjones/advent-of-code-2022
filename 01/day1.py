INPUT_FILE = '01/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            results.append(line.strip())
    return results


def find_most_calories(input):
    max_val = 0
    current_sum = 0
    for val in input:
        current_sum += int(val) if val != '' else 0
        max_val = current_sum if max_val < current_sum else max_val
        if val == '':
            current_sum = 0
    return max_val


def find_top_three_calories(input):
    totals = []
    max_val = 0
    current_sum = 0
    for val in input:
        current_sum += int(val) if val != '' else 0
        if val == '':
            totals.append(current_sum)
            current_sum = 0
    if current_sum > 0:
        totals.append(current_sum)
    totals.sort(reverse=True)
    top_three = totals[0:3]
    return sum(top_three)


if __name__ == "__main__":
    print('Day 1')
    data = fetch_input()
    total = find_top_three_calories(data)
    print(total)
