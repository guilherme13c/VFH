module top(input logic A, G, inout logic B, E, inout logic C, D, F);
    assign B = ~A;
    assign E = A + G;
    assign C = B == E;
    assign D = C & F;
    assign F = !D;
endmodule
