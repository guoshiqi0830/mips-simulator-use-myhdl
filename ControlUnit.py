from myhdl import *


@block
def ControlUnit(opCode,
                zero,
                PCWre,
                ALUSrcB,
                ALUM2Reg,
                RegWre,
                InsMemRW,
                DataMemR,
                DataMemW,
                ExtSel,
                PCSrc,
                RegOut,
                ALUOp,
                DEBUG=False):
    '''
    控制单元
    @param opCode: 输入信号，操作代码
    @param zero: 输入信号，ALU的操作结果是否为0
    @param PCWre: 控制是否转到下一条指令，halt指令执行时为0，其余为1
    @param ALUSrcB: 为1时ALU从寄存器获取数据，否则从扩展单元获取
    @param RegWre: 控制register file是否写数据
    @param InsMemRW: 控制instruction memory是否读取指令
    @param DataMemR: 控制data memory是否读取数据
    @param DataMemW: 控制data memory是否写数据
    @param ExtSel: 控制扩展单元是否扩展立即数
    @param PCSrc: 控制PC是否加上立即数，分支指令时为1，其余为0
    @param RegOut: 控制寄存器是将结果写入rt还是rd
    @param ALUOp: ALU的操作类型
    '''
    @always(opCode, zero)
    def logic():
        if DEBUG:
            print('-> Enter CU')
            print('opcode:' + '{0:06b}'.format(int(opCode)))

        PCWre.next = 0 if opCode == intbv('111111')[6:] else 1
        ALUSrcB.next = 1 if opCode in (intbv('000001')[6:],
                                       intbv('010000')[6:],
                                       intbv('100110')[6:],
                                       intbv('100111')[6:]) else 0
        ALUM2Reg.next = 1 if opCode == intbv('100111')[6:] else 0
        RegWre.next = 0 if opCode in (intbv('100110')[6:],
                                      intbv('111111')[6:]) else 1
        InsMemRW.next = 0
        #? DataMemRW.next = 0 if opCode == intbv('100111')[6:] else 1
        # 和ppt中的不同，改为了两个信号分别控制读和写
        DataMemR.next = 1 if opCode == intbv('100111')[6:] else 0
        DataMemW.next = 1 if opCode == intbv('100110')[6:] else 0
        ExtSel.next = 0 if opCode == intbv('010000')[6:] else 1
        PCSrc.next = 1 if (opCode == intbv('110000')[6:] and zero == 1) else 0
        RegOut.next = 0 if opCode in (intbv('000001')[6:], intbv('010000')[6:],
                                      intbv('100111')[6:]) else 1

        aluop = intbv(0)[3:]
        aluop[2] = 1 if opCode in (intbv('010001')[6:],
                                   intbv('101010')[6:]) else 0
        aluop[1] = 1 if opCode in (intbv('010000')[6:], intbv('010010')[6:],
                                   intbv('101010')[6:]) else 0
        aluop[0] = 1 if opCode in (intbv('000010')[6:], intbv('010000')[6:],
                                   intbv('010010')[6:],
                                   intbv('101010')[6:]) else 0
        ALUOp.next = aluop

        if DEBUG:
            print('<- Exit CU\n')

    return logic


@block
def test():
    signal_1bit = [Signal(intbv(0)[1:]) for i in range(10)]
    PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW, \
        DataMemR, DataMemW, ExtSel, PCSrc, RegOut = signal_1bit
    ALUOp = Signal(intbv(0)[3:])
    opCode = Signal(intbv('0')[6:])
    zero = Signal(0)

    cu = ControlUnit(opCode, zero, PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW,
                     DataMemR, DataMemW, ExtSel, PCSrc, RegOut, ALUOp)

    @instance
    def stimulus():
        for op_value in [
                int('100110', 2),
                int('111111', 2),
                int('010010', 2),
                int('010001', 2)
        ]:
            opCode.next = op_value
            yield delay(10)
            print('op_value:', '{0:06b}'.format(op_value))
            print(PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW, DataMemR,DataMemW,
                  ExtSel, PCSrc, RegOut, 'aluop:', '{0:03b}'.format(int(ALUOp)))

    return instances()


def main():
    t = test()
    t.run_sim()


if __name__ == '__main__':
    main()
