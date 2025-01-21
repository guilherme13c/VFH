module d_flip_flop(input clk, input rst, input data, output out);
    reg dff;
    always@(posedge clk) begin
        dff <= rst ? 1'b0 : data;
    end
    assign out = dff;
endmodule

module top(input clk, input rst, input data, output out);
    wire gclk, self;
    assign gclk = clk & self;
    d_flip_flop dff(gclk, rst, data, self);
    assign out = gclk;
endmodule
