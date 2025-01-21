module top(inout a);
    inverter inv(a, a);
endmodule

module inverter(input a, output b);
    assign b = ~a;
endmodule
