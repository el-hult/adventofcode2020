import re
from collections import defaultdict

from util import read_input

test_data = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
"""


def get_bag_map(input):
    lines = input.splitlines()
    bag_map_nodes = defaultdict(lambda: dict(holds={}, held_by=set()))
    for line in lines:
        container, contained = re.compile(" bags contain ").split(line)
        if contained != "no other bags.":
            contained = re.compile(r" bags, | bag, | bag\.| bags\.").split(contained)[
                :-1
            ]
            content = {}
            for cont in contained:
                a, b = cont.split(" ", 1)
                bag_map_nodes[b]["held_by"].add(container)
                content[b] = int(a)
        else:
            content = dict()

        bag_map_nodes[container]["holds"] = content
    return bag_map_nodes


def solve_a(bag_graph):
    n_can_hold_shiny_gold = 0
    visited = set()
    to_seek = bag_graph["shiny gold"]["held_by"].copy()
    while to_seek:
        next_bag = to_seek.pop()  # pick one parental bag
        visited.add(next_bag)  # record that it has been seen
        n_can_hold_shiny_gold += (
            1  # record that this is one bag that can eventually hold a gold bag
        )
        to_add = bag_graph[next_bag]["held_by"] - visited
        to_seek |= to_add

    return n_can_hold_shiny_gold


def get_bags_inside(graph, bag):
    to_compute = ["shiny gold"]
    computed = set()
    while to_compute:
        this_bag = to_compute.pop(0)
        content = graph[this_bag]["holds"]
        if all(bag in computed for bag in content.keys()):
            graph[this_bag]["n_inside"] = 1
            for b, c in content.items():
                graph[this_bag]["n_inside"] += c * graph[b]["n_inside"]
            computed.add(this_bag)
        else:
            to_compute.insert(-1, this_bag)  # we circulate the not-yet-computed bags
            for bag in content.keys():
                if bag not in computed and bag not in to_compute:
                    to_compute.insert(0, bag)

    return graph["shiny gold"]["n_inside"] - 1  # every node contains 1 for itself


def solve_b(bag_graph):
    return get_bags_inside(bag_graph, "shiny gold")


bag_graph = get_bag_map(test_data)
assert solve_a(bag_graph) == 4
assert solve_b(bag_graph) == 32

bag_graph = get_bag_map(read_input(7))
ansA = solve_a(bag_graph)
assert ansA < 303
assert ansA == 229
ansB = solve_b(bag_graph)
assert ansB == 6683
