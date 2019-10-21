from myhdl import *


@block
def registerFile(clk, RegWre, RegOut, rs, rt, rd, ALUM2Reg, dataFromALU,
                 dataFromRW, Data1, Data2):
    writeReg = Signal(intbv(0)[5:])
    writeData = Signal(intbv(0)[32:])
    register = [Signal(intbv(0)[32:]) for i in range(32)]

    @always_comb
    def read_reg():
        print('-> Enter read reg')
        print('RegWre:' + str(RegWre), 'RegOut:' + str(RegOut),
              'rs:' + str(rs), 'rt:' + str(rt), 'rd:' + str(rd),
              'ALUM2Reg:' + str(ALUM2Reg), 'dataFromALU:' + str(dataFromALU),
              'dataFromRW:' + str(dataFromRW))

        Data1.next = register[rs]
        Data2.next = register[rt]
        print('Read Reg -> Data1:' + str(register[rs]),
              'Data2:' + str(register[rt]))
        print('<- Exit read reg\n')

    @always(clk.negedge) # , RegOut, RegWre, ALUM2Reg, writeReg, writeData
    def write_reg():
        print('-> Enter write reg')
        # R type指令写入rd， I type指令写入rt
        writeReg = rd if RegOut else rt
        # ALUM2Reg为1则将内存的内容写入寄存器，否则将ALU的计算结果写入寄存器
        writeData = dataFromRW if ALUM2Reg else dataFromALU
        if RegWre and writeReg:
            register[writeReg] = writeData
            print('Write Reg -> register[' + str(writeReg) + ']:' +
                  str(register[writeReg]))

        print('<- Exit write reg\n')

    return read_reg, write_reg
