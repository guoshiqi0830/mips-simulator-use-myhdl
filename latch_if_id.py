from myhdl import *


def latch_if_id(clk, rst,
                pc_addr_in, op_in, rs_in, rt_in, rd_in, immediate_in,
                pc_addr_out, op_out, rs_out, rt_out, rd_out, immediate_out,
                stall=Signal(intbv(0)[1:])):
    @always(clk.posedge, rst.posedge)
    def latch():
        if rst == 1:
            pc_addr_out.next = 0
            op_out.next = 0
            rs_out.next = 0
            rt_out.next = 0
            rd_out.next = 0
            immediate_out.next = 0

        else:
            if not stall:
                pc_addr_out.next = pc_addr_in
                op_out.next = op_in
                rs_out.next = rs_in
                rt_out.next = rt_in
                rd_out.next = rd_in
                immediate_out.next = immediate_in

    return latch
