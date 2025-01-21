# Formal Connectivity Verification

# Author(s):
#
#

# Parse the CSV connectivity specification defined in the $spec variable and
# generate assertions to verify that each connection in the CSV is proven in
# the RTL implementation

if {[string compare  $argv ""] != 0} {
    set spec [lindex $argv 0]

    proc assert {args} {puts "DUMMY ASSERT: creating assertion '$args'"}
}

set spec_file [open $spec r]
set csv_lines [read $spec_file]
close $spec_file
set lines [split $csv_lines \n]

for {set i 1} {$i < [llength $lines]} {incr i} {
    set line [lindex $lines $i]
    if {[string trim $line] eq ""} { continue } ;

    set fields [split $line ,]

    set source_signal [lindex $fields 3]
    set destination_signal [lindex $fields 5]

    assert "$source_signal == $destination_signal"
}
