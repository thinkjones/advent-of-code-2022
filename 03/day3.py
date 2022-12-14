from collections import defaultdict

INPUT_FILE = '03/input.txt'


def fetch_and_decrypt_input(run_compartment_split):
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            if run_compartment_split is True:
                midpoint = int(len(full_line) / 2)
                compartment1 = full_line[0: midpoint]
                compartment2 = full_line[midpoint:]
                if len(compartment1) != len(compartment2):
                    print("ERROR")
                results.append([compartment1, compartment2])
            else:
                results.append(full_line)
    return results


def find_common_item(comp1, comp2):
    total_map = defaultdict(lambda: [0, 0])
    for i in range(0, len(comp1)):
        total_map[comp1[i]][0] = 1
        total_map[comp2[i]][1] = 1
    common_item = [k for k, v in total_map.items() if v == [1, 1]]
    return common_item[0]


def find_common_items_generic(values):
    matching_items = [1 for element in range(len(values))]
    total_map = defaultdict(lambda: [0 for element in range(len(values))])
    for arrIdx in range(0, len(values)):
        for i in range(0, len(values[arrIdx])):
            total_map[values[arrIdx][i]][arrIdx] = 1
    common_item = [k for k, v in total_map.items() if v == matching_items]
    return common_item[0]


def calc_score(character):
    char_value = ord(character)
    if char_value <= ord('Z'):
        # Uppercase
        return char_value - ord('A') + 26 + 1
    else:
        # Lowercase
        return char_value - ord('a') + 1


def find_common_items_array(input):
    results = []
    for val in input:
        char_value = find_common_item(val[0], val[1])
        # print((char_value, ord(char_value), calc_score(char_value)))
        results.append(calc_score(char_value))
    return results


def find_common_items_array_generic(input):
    results = []
    for val in input:
        char_value = find_common_items_generic(val)
        print((char_value, ord(char_value), calc_score(char_value)))
        results.append(calc_score(char_value))
    return results


def combine_by_groups(input, rows_to_group):
    return [input[i: i + 3] for i in range(0, len(input), rows_to_group)]


if __name__ == "__main__":
    # Part 1
    print('Day 3 - Part 1')
    data = fetch_and_decrypt_input(True)
    common_item_scores = find_common_items_array(data)
    print(common_item_scores)
    print(sum(common_item_scores))

    print('Day 3 - Part 2')
    data = fetch_and_decrypt_input(False)
    grouped_by_3 = combine_by_groups(data, 3)
    print(grouped_by_3)
    common_item_scores = find_common_items_array_generic(grouped_by_3)
    print(common_item_scores)
    print(sum(common_item_scores))
