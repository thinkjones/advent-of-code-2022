from collections import defaultdict

INPUT_FILE = '08/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            results.append(list(full_line))
    return results


def look_from_left(results, results_map,  total_x, total_y):
    for y in range(0, total_y):
        current_max = results[y][0]
        results_map[f'0-{y}'] = 1
        for x in range(1, total_x):
            val = results[y][x]
            if val > current_max:
                results_map[f'{x}-{y}'] += 1
                current_max = val


def look_from_right(results, results_map,  total_x, total_y):
    for y in range(0, total_y):
        current_max = results[y][total_x - 1]
        results_map[f'{total_x - 1}-{y}'] = 1
        for x in range(total_x - 1, -1, -1):
            val = results[y][x]
            if val > current_max:
                results_map[f'{x}-{y}'] += 1
                current_max = val


def look_from_top(results, results_map,  total_x, total_y):
    for x in range(0, total_x):
        current_max = results[0][x]
        results_map[f'{x}-0'] = 1
        for y in range(1, total_y):
            val = results[y][x]
            if val > current_max:
                results_map[f'{x}-{y}'] += 1
                current_max = val


def look_from_bottom(results, results_map,  total_x, total_y):
    for x in range(0, total_x):
        current_max = results[total_y - 1][x]
        results_map[f'{x}-{total_y - 1}'] = 1
        for y in range(total_y - 1, -1, -1):
            val = results[y][x]
            if val > current_max:
                results_map[f'{x}-{y}'] += 1
                current_max = val


def walk_north(results, x, y):
    value = results[y][x]
    tree_count = 0
    for y_pos in range(y - 1, -1, -1):
        current_value = results[y_pos][x]
        tree_count += 1
        if current_value >= value:
            break
    return tree_count


def walk_south(results, x, y):
    value = results[y][x]
    tree_count = 0
    for y_pos in range(y + 1, len(results)):
        current_value = results[y_pos][x]
        tree_count += 1
        if current_value >= value:
            break
    return tree_count


def walk_east(results, x, y, total_x):
    value = results[y][x]
    tree_count = 0
    for x_pos in range(x + 1, total_x):
        current_value = results[y][x_pos]
        tree_count += 1
        if current_value >= value:
            break
    return tree_count


def walk_west(results, x, y):
    value = results[y][x]
    tree_count = 0
    for x_pos in range(x - 1, -1, -1):
        current_value = results[y][x_pos]
        tree_count += 1
        if current_value >= value:
            break
    return tree_count


def calc_max_scenic_score(total_x, total_y, results):
    max_score = 0
    for y in range(0, total_y):
        for x in range(0, total_x):
            score_n = walk_north(results, x, y)
            score_s = walk_south(results, x, y)
            score_e = walk_east(results, x, y, total_x)
            score_w = walk_west(results, x, y)
            scenic_score = score_n * score_s * score_w * score_e
            max_score = scenic_score if scenic_score > max_score else max_score
    return max_score


def part_one_and_two():
    raw_results = fetch_input()
    results = raw_results
    total_x = len(results[0])
    total_y = len(results)
    print(total_x, total_y)

    # Part 1
    results_map = defaultdict(int)
    look_from_left(results, results_map, total_x, total_y)
    look_from_right(results, results_map, total_x, total_y)
    look_from_top(results, results_map, total_x, total_y)
    look_from_bottom(results, results_map, total_x, total_y)
    print(results_map)
    print(len(results_map.keys()))

    # Part 2
    max_score = calc_max_scenic_score(total_x, total_y, results)
    print(max_score)


if __name__ == "__main__":
    part_one_and_two()
