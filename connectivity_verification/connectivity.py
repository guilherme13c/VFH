"""
Structural Connectivity Verification

Author(s):
    -
    -

Parse the JSON netlist file and the CSV connectivity specification and traverse
the netlist to verify that each connection in the CSV is reachable in the RTL
implementation.

Some connections might not be verified because their circuits have
combinational loops. These must be detected and reported as well.
"""

import netlist as nl

import csv
import json
import sys


class Finder(nl.Visitor):
    def __init__(self, netlist: nl.Netlist, search: nl.Net):
        super().__init__(netlist, nl.Direction.FORWARD, nl.Algorithm.BFS)
        self.visited = set()
        self.found = False
        self.search = search

    def visit(self, net: nl.Net) -> bool:
        if net in self.visited:
            return False
        self.visited.add(net)
        if self.search == net:
            self.found = True
            return False
        return True

    def visit_gate(self, gate: nl.Gate) -> list:
        if gate in self.visited:
            return list()
        self.visited.add(gate)
        return self.get_next_nodes(gate)


class LoopDetector(nl.Visitor):
    def __init__(self, netlist: nl.Netlist, start: nl.Net):
        super().__init__(netlist, nl.Direction.BACKWARD, nl.Algorithm.DFS)
        self.start = start
        self.visited = set()
        self.recursion_stack = set()
        self.has_combinational_loop = False

    def visit(self, net: nl.Net) -> bool:
        if net in self.visited:
            if net in self.recursion_stack:
                self.has_combinational_loop = True
            return False
        self.visited.add(net)
        self.recursion_stack.add(net)
        return True

    def visit_gate(self, gate: nl.Gate) -> list:
        if gate.type == "$dff":
            return gate.get_clock()
        return self.get_next_nodes(gate)
    
    def get_next_nodes(self, node):
        if self.direction == nl.Direction.FORWARD:
            return node.outputs
        elif self.direction == nl.Direction.BACKWARD:
            return node.inputs
        elif self.direction == nl.Direction.BIDIRECTIONAL:
            return node.inputs + node.outputs

    def post_visit(self, net: nl.Net):
        # Remove the net from the recursion stack after backtracking
        self.recursion_stack.discard(net)



def main():
    try:
        json_netlist_file = sys.argv[1]
    except IndexError:
        print("Error: missing input JSON netlist file")
        exit(1)

    try:
        csv_spec_file = sys.argv[2]
    except IndexError:
        print("Error: missing input CSV spec file")
        exit(1)

    connectionsToVerify = list()
    with open(csv_spec_file, 'r') as csf:
        reader = csv.reader(csf)
        for line in reader:
            connectionsToVerify.append(
                (
                    line[1],
                    line[3],
                    line[5],
                )
            )
    connectionsToVerify.pop(0)

    with open(json_netlist_file) as jnf:
        rtl = nl.RTL(json.load(jnf))

        for conn in connectionsToVerify:
            for netlist in rtl.netlists:
                start = netlist.find_net(conn[1].strip("!~")+"[0]")
                end = netlist.find_net(conn[2].strip("!~")+"[0]")
                if start and end:
                    visitor = Finder(
                        netlist,
                        end,
                    )
                    visitor.traverse(start)

                    loop_detector = LoopDetector(
                        netlist,
                        start,
                    )
                    loop_detector.traverse(start)

                    if loop_detector.has_combinational_loop:
                        print(f"{conn[0]} combinational_loop")
                    elif visitor.found:
                        print(f"{conn[0]} connected")
                    else:
                        print(f"{conn[0]} unconnected")
                else: print("NotFound")


if __name__ == "__main__":
    main()
