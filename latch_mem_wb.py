from myhdl import *


def latch_mem_wb(clk, rst, 
                 ram_in, alu_result_in, 
                 RegWre_in, ALUM2Reg_in, RegOut_in
                 ram_out, alu_result_out, 
                 RegWre_out, ALUM2Reg_out, RegOut_out
                ):

    @always(clk.posedge, rst.posedge)
    def latch():
        if rst == 1:
            ram_out.next = 0
            alu_result_out.next = 0
            RegWre_out.next = 0
            ALUM2Reg_out.next = 0
            RegOut_out.next = 0
        else:
            ram_out.next = ram_in
            alu_result_out.next = alu_result_in
            RegWre_out.next = RegWre_in
            ALUM2Reg_out.next = ALUM2Reg_in
            RegOut_out.next = RegOut_in

    return latch