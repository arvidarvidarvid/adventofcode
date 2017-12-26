import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_input(filename='day.input'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


class PortTree(object):

    def __init__(self, raw_ports):
        self.parent = None
        self.raw_ports = raw_ports
        self.children = []

    def populate_tree(self):
        for id, port in self.raw_ports.items():
            if port[0] == 0:
                self.children.append(Port(id, port[0], port[1], self))
            elif port[1] == 0:
                self.children.append(Port(id, port[1], port[0], self))
        for child in self.children:
            child.populate_children(self.raw_ports)

    def leafs(self):
        leafs = []
        for child in self.children:
            leafs += child.leafs()
        return leafs

    def highest_strength(self):
        return max([p.strength(self.raw_ports) for p in self.leafs()])

    def longest_strongest(self):
        _candidates = sorted([(port.length(), port.strength(self.raw_ports))
                              for port in self.leafs()], reverse=True)
        _longest_strongest = _candidates[0]
        print(_longest_strongest)
        return _longest_strongest[1]


class Port(object):

    def __init__(self, id, parent_pin, child_pin, parent):
        self.id = id
        self.parent_pin = parent_pin
        self.child_pin = child_pin
        self.parent = parent
        self.children = []

    def __str__(self):
        return ', '.join([
            str(self.id), str(self.parent_pin), str(self.child_pin)])

    def parents(self):
        parent = self.parent
        ids = []
        while parent.parent is not None:
            ids.append(parent.id)
            parent = parent.parent
        ids += [self.id]
        return ids

    def populate_children(self, raw_ports):
        _parents = self.parents()
        for id, port in raw_ports.items():
            if id not in _parents:
                if port[0] == self.child_pin:
                    self.children.append(Port(id, port[0], port[1], self))
                if port[1] == self.child_pin:
                    self.children.append(Port(id, port[1], port[0], self))
        for child in self.children:
            child.populate_children(raw_ports)

    def leafs(self):
        if self.children == []:
            return [self]
        else:
            return [l for c in self.children for l in c.leafs()]

    def strength(self, raw_ports):
        return sum([raw_ports[id][0] + raw_ports[id][1]
                    for id in self.parents()])

    def length(self):
        return len(self.parents())


def get_port_tree(input):
    raw_ports = {id: [int(i) for i in l.split('/')]
                 for id, l in enumerate(input)}
    return PortTree(raw_ports)


def test():
    test_input = get_input('test.input')
    tree = get_port_tree(test_input)
    tree.populate_tree()
    assert tree.highest_strength() == 31
    assert tree.longest_strongest() == 19
    logger.info('Tests passed')


def main():
    input = get_input()
    tree = get_port_tree(input)
    tree.populate_tree()
    logger.info('Result 1: %s' % tree.highest_strength())
    logger.info('Result 2: %s' % tree.longest_strongest())


if __name__ == '__main__':
    test()
    main()
