#!/bin/bash

for testcase in ./*.v; do
    jasper_script="\
        catch {set_terminal_colored_output on}
        analyze -sv12 ${testcase};
        elaborate;
        clock -none;
        reset -none;
        include ../connectivity.tcl;
        foreach property [get_property_list] {
            set property_expr [get_property_info \$property -list expression]
            puts \"\n\nProving property \$property_expr\"
            catch {puts \n[prove -property \$property]}
        }
    "

    echo "Running Formal Connectivity Verification for ${testcase}"
    jg -batch -allow_unsupported_OS -acquire_proj \
        -command "${jasper_script}" \
        -define rtl "${testcase}" \
        -define spec "${testcase%.v}.csv"

    yosys_script="\
        read -sv2012 ${testcase};
        prep -top top;
        hierarchy -check;
        memory -nomap;
        flatten;
        write_json ${testcase%.v}.json;
    "

    echo "Compiling ${testcase}"
    yosys -q -p "${yosys_script}"

    echo "Running Structural Connectivity Verification for ${testcase}"
    python3 ../connectivity.py ${testcase%.v}.json ${testcase%.v}.csv
done
