module top(inout a0, inout a1, inout a2);
    fully_connected inst(.*);
endmodule

module fully_connected(inout a0, inout a1, inout a2);
    wire d0;
    wire b0, b1, b2;
    assign b0 = d0 & a2;
    assign a1 = a0 & b0;
    assign b1 = a1 & a2;
    assign a0 = d0 & b1;
    assign b2 = a1 & a0;
    assign a2 = b2 & d0;
endmodule
