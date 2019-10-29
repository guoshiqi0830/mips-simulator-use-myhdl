from myhdl import *

def latch_ex_mem(clk, rst, 
                pc_addr_in, zero_in, alu_result_in, data2_in,
                DataMemR_in, DataMemW_in, PCSrc_in, RegWre_in, ALUM2Reg_in, RegOut_in,
                pc_addr_out, zero_out, alu_result_out, data2_out,
                DataMemR_out, DataMemW_out, PCSrc_out, RegWre_out, ALUM2Reg_out, RegOut_out
                ):

    @always(clk.posedge, rst.posedge)
    def latch():
        if rst == 1:
            pc_addr_out.next = 0
            zero_out.next = 0
            alu_result_out.next = 0
            data2_out.next = 0
            DataMemR_out.next = 0
            DataMemW_out.next = 0
            PCSrc_out.next = 0
            RegWre_out.next = 0
            ALUM2Reg.next = 0
            RegOut_out.next = 0
        else:
            pc_addr_out.next = pc_addr_in
            zero_out.next = zero_in
            alu_result_out.next = alu_result_in
            data2_out.next = data2_in
            DataMemR_out.next = DataMemR_in
            DataMemW_out.next = DataMemW_in
            PCSrc_out.next = PCSrc_in
            RegWre_out.next = RegWre_in
            ALUM2Reg_out.next = ALUM2Reg_in
            RegOut_out.next = RegOut_in


    return latch