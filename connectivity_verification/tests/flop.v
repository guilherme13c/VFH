module top
(
    input logic clk, rstn,
    input logic [3:0] A,
    output logic [3:0] sum,
    output logic carry
);
    logic [3:0] flop_out;
    flop flop_inst(clk, rstn, A, flop_out);
    adder adder_inst(clk, rstn, flop_out, sum, carry);
endmodule

module flop
(
    input logic clk, rstn,
    input logic [3:0] in,
    output logic [3:0] out
);
    always @(posedge clk)
        if (~rstn) out = 1'b0;
        else out = in;
endmodule

module adder
(
    input logic clk, rstn,
    input logic [3:0] in,
    output logic [3:0] sum,
    output logic carry
);
    logic [4:0] tmp_sum;
    assign tmp_sum = sum + in;
    assign carry = tmp_sum[4];
    always @(posedge clk) begin
        if (~rstn) begin
            sum = 1'b0;
        end else begin
            sum = tmp_sum;
        end
    end
endmodule
