import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class Node(object):

    def __init__(self, identifier, value=None, parent=None, children=[]):
        self.identifier = identifier
        self.value = value
        self.parent = parent
        self.children = []

    def total_weight(self):
        return int(self.value) + sum([c.total_weight() for c in self.children])


class NodeSet(object):

    def __init__(self):

        self.lookup = {}
        self.last_seen_identifier = None

    def get_or_create_node(self, identifier):
        self.last_seen_identifier = identifier
        if identifier in self.lookup:
            return self.lookup[identifier]
        else:
            self.lookup[identifier] = Node(identifier)
            return self.get_or_create_node(identifier)

    def get_top_parent(self, identifier=None):
        if identifier is None:
            identifier = self.last_seen_identifier
        node = self.get_or_create_node(identifier)
        if node.parent is None:
            return node
        else:
            return self.get_top_parent(node.parent.identifier)

    def populate_nodes_from_input(self, input):
        for line in input:
            line_parts = line.split(' -> ')
            primary_node = line_parts[0]
            if len(line_parts) > 1:
                children = line_parts[1]
            else:
                children = ''
            node_components = re.match(r'(.+) \((\d+)\)', primary_node.strip())
            identifier = node_components[1]
            value = node_components[2]
            node = self.get_or_create_node(identifier)
            node.value = value
            if children:
                for child in children.split(','):
                    child = self.get_or_create_node(child.strip())
                    child.parent = node
                    node.children.append(child)

    def find_imbalanced_node(self, node):
        weights = [c.total_weight() for c in node.children]
        if len(set(weights)) == 1:
            return node
        else:
            for c in node.children:
                if c.total_weight != sorted(weights)[1]:
                    return self.find_imbalanced_node(c)

    def find_rebalance_value(self, node):
        siblings = node.parent.children
        most_common_value = sorted([c.total_weight() for c in siblings])[1]
        adjustment_needed = node.total_weight() - most_common_value
        new_value = int(node.value) - adjustment_needed
        return new_value


def test():
    test_input = get_input('test.input')
    node_set = NodeSet()
    node_set.populate_nodes_from_input(test_input)
    top_parent = node_set.get_top_parent(node_set.last_seen_identifier)
    assert top_parent.identifier == 'tknk'
    imbalanced_node = node_set.find_imbalanced_node(top_parent)
    assert imbalanced_node.identifier == 'ugml'
    assert node_set.find_rebalance_value(imbalanced_node) == 60
    logger.info('Tests passed')


def main():

    input = get_input()

    node_set = NodeSet()
    node_set.populate_nodes_from_input(input)
    top_parent = node_set.get_top_parent()
    imbalanced_node = node_set.find_imbalanced_node(top_parent)
    logger.info('Result 1: %s' % top_parent.identifier)
    logger.info('Result 2: %s' % node_set.find_rebalance_value(
        imbalanced_node))


if __name__ == '__main__':
    test()
    main()
