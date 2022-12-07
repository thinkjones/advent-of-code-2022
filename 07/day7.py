from collections import defaultdict

INPUT_FILE = '07/input.txt'


def fetch_input():
    results = []
    # open the file and read its contents
    with open(INPUT_FILE) as file:
        # iterate over each line in the file
        for line in file:
            # append the line to the list, stripping any whitespace characters
            # from the beginning and end of the line
            full_line = line.rstrip('\n')
            results.append(full_line)
    return results


class Node(object):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.depth = parent.depth + 1 if parent else 0
        self.child = []
        self.file_total = 0
        self.dir_total = 0
        self.total = 0

    def get_child(self, name):
        return [c for c in self.child if c.name == name][0]


def populate_tree(results):
    root_node = Node('/', None)
    current_node = root_node
    print(results)

    for item in results:
        dir_total = 0
        if item == '$ cd /':
            current_node = root_node
        elif item == '$ ls':
            continue
        elif item[0:3] == 'dir':
            dir_name = item[4:]
            current_node.child.append(Node(dir_name, current_node))
        elif item[0:7] == '$ cd ..':
            change_dir = current_node.parent.name
            current_node = current_node.parent
        elif item[0:4] == '$ cd':
            change_dir = item[5:]
            current_node = current_node.get_child(change_dir)
        else:
            file_details = item.split(' ')
            current_node.file_total += int(file_details[0])
    return root_node


def recurse_dirs_to_add_dir_total(node):
    if len(node.child) == 0:
        # No more child directories display size
        node.total = node.file_total + node.dir_total
        return node.file_total
    else:
        node.dir_total = 0
        for c in node.child:
            node.dir_total += recurse_dirs_to_add_dir_total(c)
        node.total = node.file_total + node.dir_total
        return node.total


def find_dirs_with_at_most_100k(node, results_array):
    if node.total <= 100000:
        results_array.append(node)

    if len(node.child) > 0:
        for c in node.child:
            find_dirs_with_at_most_100k(c, results_array)


def find_smallest_dir_required(node, smallest_node=None, min_space_needed=0):
    if node.total >= min_space_needed and (smallest_node is None or smallest_node.total > node.total):
        smallest_node = node

    if len(node.child) > 0:
        for c in node.child:
            smallest_node = find_smallest_dir_required(c, smallest_node, min_space_needed)

    return smallest_node


def part_one():
    results = fetch_input()
    root_node = populate_tree(results)
    results_array = []
    recurse_dirs_to_add_dir_total(root_node)
    find_dirs_with_at_most_100k(root_node, results_array)
    print(len(results_array))
    totals = [n.total for n in results_array]
    print(totals)
    print(sum(totals))

    total_filespace = 70000000
    required_unusedspace = 30000000

    total_used_space = root_node.total
    print(f'Total used: {total_used_space}')
    total_available = total_filespace - root_node.total
    print(f'Total available: {total_available}')
    extra_space_needed = required_unusedspace - total_available
    print(f'Min extra needed: {extra_space_needed}')
    smallest_node = root_node
    smallest_node = find_smallest_dir_required(root_node, smallest_node, extra_space_needed)
    print(f'Smallest dir: {smallest_node.name}-{smallest_node.total}')













if __name__ == "__main__":
    part_one()
