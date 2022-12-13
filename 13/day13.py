import heapq as heap
from collections import defaultdict
import json

INPUT_FILE = '13/input.txt'

# Distress Signal
# Packets decoded out of order, re-order packets (input)



def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            if full_line != '':
                results.append(json.loads(full_line))
    return results

def ensure_array(val):
    if type(val) == list:
        return val
    else:
        return [val]

def extract_array_val(val, idx):
    return None if idx >= len(val) else val[idx]

def either_is_array(lval, rval):
    return type(lval) == list or type(rval) == list

DEBUG = False
def debug_print(msg):
    if DEBUG:
        print(msg)

def is_left_smaller(lval, rval):
    lval = ensure_array(lval)
    rval = ensure_array(rval)
    result = None
    finished = False
    idx = 0
    while not finished:
        curr_lval = extract_array_val(lval, idx)
        curr_rval = extract_array_val(rval, idx)

        if result is False:
            debug_print('ended')
            return result
        elif curr_lval is None or curr_rval is None:
            debug_print('either val is None')
            # End as we've ended lists
            if result is None:
                debug_print('result is None')
                result = False if curr_rval is None and curr_lval is not None else True
            elif curr_lval is not None and curr_rval is None:
                debug_print(f'No right val: {result}')
                result = False if result is None else result
            finished = True
        elif either_is_array(curr_lval, curr_rval):
            debug_print('either is array')
            result = is_left_smaller(curr_lval, curr_rval)
            if result == True:
                finished = True
            debug_print(f'Sub {idx} - {result}')
        elif curr_rval < curr_lval:
            debug_print(f'rval is less than lval {curr_lval}-{curr_rval}')
            # Right val less than left val
            result = False
            finished = True
        elif curr_rval == curr_lval:
            result = None if result is None else result
        else:
            debug_print('calc result')
            result = True
            finished = True
        idx += 1
    print(f'Analyzing: run_test({json.dumps(lval)}, {json.dumps(rval)}) -> {result}')
    return result


def run_test(lval, rval, expected):
    result = is_left_smaller(lval, rval)
    test_success = 'WRONG' if result != expected else 'CORRECT'
    print(f'test_success: {test_success} value expected {expected}\n\n')

def test_cases():
    run_test([[2], 9], [3], True)
    run_test([2, 3, 4], [4], True)
    run_test([], [8], True)
    run_test([[], 2, 9, 4], [[8], [3, 6, 9, [10, 4, 2], [4, 5]], [10, [3], [7, 10, 7, 2], [0, 5]], 2], True)

def test_cases_all():
    run_test([1,1,3,1,1], [1,1,5,1,1], True)
    run_test([1], [1], True)
    run_test([[1],[2,3,4]], [[1],4], True)
    run_test([9], [[8,7,6]], False)
    run_test([[4,4],4,4], [[4,4],4,4,4], True)
    run_test([7,7,7,7], [7,7,7], False)
    run_test([], [3], True)
    run_test([[[]]], [[]], False)
    run_test([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9], False)
    run_test([[2], 9], [3], True)


def part_one():
    raw_results = fetch_input()
    print(len(raw_results))
    correct_order = []
    for count in range(0, int(len(raw_results)/2)):
        left_idx = count * 2
        right_idx = left_idx + 1
        left_val = raw_results[left_idx]
        right_val = raw_results[right_idx]
        print(f'*** Pair {count}')
        result = is_left_smaller(left_val, right_val)
        print(f'{result}\n\n')
        if result:
            correct_order.append(count + 1)

    print(correct_order)
    print(sum(correct_order))





if __name__ == "__main__":
    part_one()

