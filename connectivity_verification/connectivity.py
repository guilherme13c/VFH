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
    def __init__(self, netlist: nl.Netlist, direction: nl.Direction, algorithm: nl.Algorithm, search: nl.Net):
        super().__init__(netlist, direction, algorithm)
        self.visited = set()
        self.found = False
        self.search = search

    def visit(self, net: nl.Net) -> bool:
        if net in self.visited:
            return False
        self.visited.add(net)
        print(f"visiting net {net}")
        if self.search == net:
            self.found = True
            return False
        return True

    def visit_gate(self, gate: nl.Gate) -> list:
        if gate in self.visited:
            return list()
        self.visited.add(gate)
        print(f"visiting gate {gate}")
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

    connectionsToVerify = list()
    with open(csv_spec_file, 'r') as csf:
        reader = csv.reader(csf)
        for line in reader:
            connectionsToVerify.append(
                (
                    line[3],
                    line[5],
                )
            )
    connectionsToVerify.pop(0)

    # print(connectionsToVerify)

    with open(json_netlist_file) as jnf:
        rtl = nl.RTL(json.load(jnf))
        print(rtl)

        for conn in connectionsToVerify:
            for netlist in rtl.netlists:
                # print(f"netlist {netlist}")
                start = netlist.find_net(conn[0]+"[0]")
                end = netlist.find_net(conn[1]+"[0]")
                # print(start)
                # print(end)
                if start and end:
                    visitor = Finder(
                        netlist,
                        nl.Direction.FORWARD,
                        nl.Algorithm.BFS,
                        end,
                    )
                    visitor.traverse(start)
                    print(visitor.found)


if __name__ == "__main__":
    main()
