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
    signal_1bit = [Signal(intbv(0)[1:]) for i in range(9)]
    PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW, \
        DataMemRW, ExtSel, PCSrc, RegOut = signal_1bit
    ALUOp = Signal(intbv(0)[3:])
    opCode = Signal(intbv('0')[6:])
    zero = Signal(0)

    cu = ControlUnit(opCode, zero, PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW,
                     DataMemRW, ExtSel, PCSrc, RegOut, ALUOp)

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
            print(format(op_value, '#b'))
            print(PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW, DataMemRW,
                  ExtSel, PCSrc, RegOut, format(int(ALUOp), '#b'))

    return instances()


def main():
    t = test()
    t.run_sim()


if __name__ == '__main__':
    main()
