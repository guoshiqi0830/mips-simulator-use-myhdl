from myhdl import *


@block
def registerFile(clk, RegWre, RegOut, rs, rt, rd, ALUM2Reg, 
                 dataFromALU, dataFromRW, Data1, Data2):

    @always(clk.posedge, RegOut, RegWre, ALUM2Reg, writeReg, writeData)
    def logic():
        writeReg.next = rd if RegOut else rt
        writeData.next = dataFromRW if ALUM2Reg else dataFromALU
        register = [Signal(intbv(0)[32:] for i in range(32)]
        Data1.next = register[rs]
        Data2.next = register[rt]
        if RegWre and writeReg:
            register[writeReg] = writeData
    return logic

@block
def test():
    # TODO
