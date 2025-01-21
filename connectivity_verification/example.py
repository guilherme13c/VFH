# (C) 2024 Cadence Design Systems, Inc. All rights reserved worldwide.

"""
An example traversal implemented using netlist.Visitor.

Search a net name in the Netlist ("A[0]") and do a bidirectional DFS from it.
Print the name for every Net and Gate visited.
"""

import netlist as nl
import json
import sys

class ExampleVisitor(nl.Visitor):
    def __init__(self, netlist : nl.Netlist, direction : nl.Direction, algorithm : nl.Algorithm):
        super().__init__(netlist, direction, algorithm)
        self.visited = set()

    def visit(self, net : nl.Net) -> bool:
        if net in self.visited:
            return False
        self.visited.add(net)
        print("visit: {}".format(net))
        return True

    def visit_gate(self, gate : nl.Gate) -> list:
        if gate in self.visited:
            return list()
        self.visited.add(gate)
        print("visit_gate: {}".format(gate))
        return self.get_next_nodes(gate)

def main():
    try:
        json_netlist_file = sys.argv[1]
    except IndexError:
        print("Error: missing input JSON netlist file")
        exit(1)

    with open(json_netlist_file) as file:
        rtl = nl.RTL(json.load(file))
        print("Loaded RTL: {}\n".format(rtl))

        for netlist in rtl.netlists:
            start = netlist.find_net("A[0]")
            if start:
                visitor = ExampleVisitor(netlist, nl.Direction.BIDIRECTIONAL, nl.Algorithm.DFS)
                print("Running Traversal from Net: {}".format(start))
                visitor.traverse(start)

if __name__ == "__main__":
    main()
