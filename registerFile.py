from myhdl import *


@block
def registerFile(clk, RegWre, RegOut, rs, rt, rd, ALUM2Reg, 
                 dataFromALU, dataFromRW, Data1, Data2):
    writeReg = Signal(intbv(0)[5:])
    writeData = Signal(intbv(0)[32:])
    register = [Signal(intbv(0)[32:]) for i in range(32)]

        

    @always(clk.posedge, RegOut, RegWre, ALUM2Reg, writeReg, writeData)
    def logic():
        print('Enter reg file')
        print(RegWre, RegOut, rs, rt, rd, ALUM2Reg, dataFromALU, dataFromRW)
        writeReg = rd if RegOut else rt
        writeData = dataFromRW if ALUM2Reg else dataFromALU
        Data1.next = register[rs]
        Data2.next = register[rt]
        print(writeReg)
        print('Data1:' + str(register[rs]))
        print('Data2:' + str(register[rt]))
        print('Exit read reg\n')
        if RegWre and writeReg:
            register[writeReg] = writeData
            print('writeReg:' + str(writeReg))
            print('register[writeReg]:' + str(register[writeReg]) )
        print('Exit reg file\n')
    
    return logic
