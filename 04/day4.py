from collections import defaultdict

INPUT_FILE = '04/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n').split(',')
            items = [[int(val) for val in v.split('-')] for v in full_line]
            results.append(items)
    return results


def is_enclosed(arr1, arr2):
    return arr1[0] <= arr2[0] and arr1[1] >= arr2[1]


def count_fully_enclosed(input):
    results = []
    for val in input:
        enclosed = is_enclosed(val[0], val[1]) or is_enclosed(val[1], val[0])
        if enclosed:
            results.append(val)
    return results


if __name__ == "__main__":
    # Part 1
    print('Day 4 - Part 1')
    data = fetch_input()
    total = count_fully_enclosed(data)
    print(len(total))

