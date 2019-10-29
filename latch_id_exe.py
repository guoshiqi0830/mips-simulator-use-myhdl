from myhdl import *


def latch_id_ex(clk, rst,
                pc_addr_in, data1_in, data2_in, rs_in, rt_in, rd_in, ALUSrcB_in, ALUM2Reg_in,
                RegWre_in, DataMemR_in, DataMemW_in, ExtSel_in, PCSrc_in, RegOut_in, ALUOp_in,
                pc_addr_out, data1_out, data2_out, rs_out, rt_out, rd_out, ALUSrcB_out, ALUM2Reg_out,
                RegWre_out, DataMemR_out, DataMemW_out, ExtSel_out, PCSrc_out, RegOut_out, ALUOp_out
                ):

    @always(clk.posedge, rst.posedge)
    def latch():
        if rst == 1:
            pc_addr_out.next = 0
            data1_out.next = 0
            data2_out.next = 0
            rs_out.next = 0
            rt_out.next = 0
            rd_out.next = 0
            ALUSrcB_out.next = 0
            ALUM2Reg_out.next = 0
            RegWre_out.next = 0
            DataMemR_out.next = 0
            DataMemW_out.next = 0
            ExtSel_out.next = 0
            PCSrc_out.next = 0
            RegOut_out.next = 0
            ALUOp_out.next = 0
        else:
            pc_addr_out.next = pc_addr_out
            data1_out.next = data1_out
            data2_out.next = data2_out
            rs_out.next = rs_out
            rt_out.next = rt_out
            rd_out.next = rd_out
            ALUSrcB_out.next = ALUSrcB_out
            ALUM2Reg_out.next = ALUM2Reg_out
            RegWre_out.next = RegWre_out
            DataMemR_out.next = DataMemR_out
            DataMemW_out.next = DataMemW_out
            ExtSel_out.next = ExtSel_out
            PCSrc_out.next = PCSrc_out
            RegOut_out.next = RegOut_out
            ALUOp_out.next = ALUOp_out

    return latch