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
    def __init__(self, netlist: nl.Netlist, direction: nl.Direction, algorithm: nl.Algorithm):
        super().__init__(netlist, direction, algorithm)
        self.visited = set()

    def visit(self, net: nl.Net) -> bool:
        if net in self.visited:
            return False
        self.visited.add(net)
        return True

    def visit_gate(self, gate: nl.Gate) -> list:
        if gate in self.visited:
            return list()
        self.visited.add(gate)
        return self.get_next_nodes(gate)


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

    # Your code goes here
    connectionsToVerify = list()
    with open(csv_spec_file, 'r') as csf:
        csf.readline()
        for line in csf:
            vs = line.split(',')
            connectionsToVerify.append(
                (vs[3].strip(" \n"), vs[5].strip(" \n")))

    print(connectionsToVerify)

    with open(json_netlist_file) as jnf:
        rtl = nl.RTL(json.load(jnf))

        for conn in connectionsToVerify:
            for netlist in rtl.netlists:
                start = netlist.find_net(conn[0]+"[0]")
                if start:
                    visitor = Finder(
                        netlist, nl.Direction.FORWARD, nl.Algorithm.BFS)
                    visitor.traverse(start)


if __name__ == "__main__":
    main()
