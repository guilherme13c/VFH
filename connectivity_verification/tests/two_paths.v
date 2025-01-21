module top(inout a0, inout a1, inout a2, inout a3);
    two_paths t(.*);
endmodule

module two_paths(inout a0, inout a1, inout a2, inout a3);
    assign a1 = a0;
    assign a2 = a0;
    assign a3 = ~a1 + a2;
    assign a0 = ~a3;
endmodule
