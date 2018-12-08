import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return list(map(int, [line.strip()
                              for line in file.readlines()][0].split(' ')))


class Node(object):

    def __init__(self):
        self.children = []
        self.metadata = []
        self.length = None

    def total_sum_metadata(self):
        return sum(self.metadata) + sum([c.total_sum_metadata()
                                         for c in self.children])

    def total_sum_referenced_nodes(self):
        if self.children == []:
            return sum(self.metadata)
        else:
            total = 0
            for ref in self.metadata:
                try:
                    total += self.children[ref - 1].total_sum_referenced_nodes()
                except IndexError:
                    pass
            return total


def numbers_to_node(numbers):

    node = Node()

    n_children = numbers[0]
    n_metadata = numbers[1]

    children_offset = 2

    for child_node in range(n_children):
        child_node = numbers_to_node(numbers[children_offset:])
        node.children.append(child_node)
        children_offset += child_node.length

    node.metadata = numbers[children_offset:children_offset+n_metadata]
    node.length = children_offset + n_metadata

    return node


def p1(puzzle_input):
    top_node = numbers_to_node(puzzle_input)
    return top_node.total_sum_metadata()


def p2(puzzle_input):
    top_node = numbers_to_node(puzzle_input)
    return top_node.total_sum_referenced_nodes()


def test():
    test_input_p1 = get_input('test_p1.input')
    assert p1(test_input_p1) == 138
    assert p2(test_input_p1) == 66
    logger.info('Tests passed')


def main():

    puzzle_input = get_input()

    logger.info('Result 1: %s' % p1(puzzle_input))
    logger.info('Result 2: %s' % p2(puzzle_input))


if __name__ == '__main__':
    test()
    main()
