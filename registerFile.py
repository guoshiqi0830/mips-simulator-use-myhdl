from myhdl import *


@block
def registerFile(clk,RegWre,RegOut,rs,rt,rd,ALUM2Reg,dataFromALU,
                 dataFromRW,Data1,Data2,DEBUG=False):
    '''
    寄存器文件单元
    :param clk:时钟控制
    :param RegWre: 0读取,非0时写入
    :param RegOut: true，写入rd，否则rt
    :param rs: 操作数1
    :param rt: 操作数2
    :param rd: 结果
    :param ALUM2Reg:true，写数据为dataFromALU，否则为dataFromRW
    :param dataFromALU:
    :param dataFromRW:
    :param Data1:数据1
    :param Data2:数据2
    :param DEBUG:
    :return:
    '''
    writeReg = Signal(intbv(0)[5:])
    writeData = Signal(intbv(0)[32:])
    register = [Signal(intbv(0)[32:]) for i in range(32)]

    @always(RegWre, RegOut, rs, rt, rd)
    def read_reg():
        if DEBUG:
            print('-> Enter read reg')
            print('RegWre:' + str(RegWre), 'RegOut:' + str(RegOut),
                  'rs:' + str(rs), 'rt:' + str(rt), 'rd:' + str(rd),
                  'ALUM2Reg:' + str(ALUM2Reg),
                  'dataFromALU:' + str(dataFromALU),
                  'dataFromRW:' + str(dataFromRW))

        Data1.next = register[rs]
        Data2.next = register[rt]

        if DEBUG:
            print('Read Reg -> Data1:' + str(register[rs]),
                  'Data2:' + str(register[rt]))
            print('Curr Reg:')
            print('0:' + str(register[0]))
            print('1:' + str(register[1]))
            print('2:' + str(register[2]))
            print('3:' + str(register[3]))
            print('4:' + str(register[4]))
            print('<- Exit read reg\n')

    @always(clk.negedge)  # , RegOut, RegWre, ALUM2Reg, writeReg, writeData
    def write_reg():
        if DEBUG:
            print('-> Enter write reg')
            print('RegWre:' + str(RegWre), 'RegOut:' + str(RegOut),
                  'rs:' + str(rs), 'rt:' + str(rt), 'rd:' + str(rd),
                  'ALUM2Reg:' + str(ALUM2Reg),
                  'dataFromALU:' + str(dataFromALU),
                  'dataFromRW:' + str(dataFromRW))

        # R type指令写入rd， I type指令写入rt
        writeReg = rd if RegOut else rt
        # ALUM2Reg为1则将内存的内容写入寄存器，否则将ALU的计算结果写入寄存器
        writeData = Signal(
            intbv(int(dataFromRW if ALUM2Reg else dataFromALU))[32:])
        if RegWre and writeReg:
            register[writeReg] = writeData

        if DEBUG:
            print('Curr Reg:')
            print('0:' + str(register[0]))
            print('1:' + str(register[1]))
            print('2:' + str(register[2]))
            print('3:' + str(register[3]))
            print('4:' + str(register[4]))
            print('<- Exit write reg\n')

    return read_reg, write_reg
