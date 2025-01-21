# Introduction to Hardware Verification
## Connectivity Verification

Connectivity Verification on RTL using Jasper and structural Netlist traversal.
Python netlist graph traversal based on
[YosysHQ](https://github.com/YosysHQ/yosys)'s JSON netlist format.

### Work evaluation
1. Implement TCL script for Jasper Connectivity Verification at
connectivity.tcl.
2. Implement Python script for structural Netlist Verification at
connectivity.py.
3. Run all test cases in 'tests' folder:
```
cd tests
./run.sh
```
4. All connections must be either 'proven' or fail with '(ENL024):
Combinational loop found' or '(WCK008): Flop "dff" has a loop through its clock
pin.' in Jasper.
5. All proven properties must be confirmed by the structural netlist traversal.
6. All failing properties due to combinational loops must be reported by the
structural netlist traversal.

### How to use
1. Requirements:
    - Python >= 3.5.0
    - yosys >= 0.34

2. Run yosys to compile HDL file into JSON netlist format:

```
# Example yosys.ys script file
read -sv2012 example.sv
prep -top top
hierarchy -check
memory -nomap
flatten
write_json netlist.json
```

```
# Compiles 'example.sv' and generates 'netlist.json'
$ yosys yosys.ys
```

3. Instantiate a Python RTL object with the JSON netlist:

```
import json
import netlist as nl

with open("netlist.json") as netlist_file:
    rtl = nl.RTL(json.load(netlist_file))
    print(rtl)
```

4. Create a custom visitor deriving from `netlist.Visitor` to run Netlist
traversal:

```
for netlist in rtl.netlists:
    start = netlist.find_net("A[0]")
    if start:
        visitor = CustomVisitor(netlist, nl.Direction.FORWARD,
                                nl.Algorithm.BFS)
        visitor.traverse(start)
```

Run `python3 example.py <JSON_NETLIST_FILE>` for an example application.
