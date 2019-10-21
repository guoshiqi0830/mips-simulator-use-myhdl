from myhdl import *
from ALU import ALU
from Clock import Clock
from ControlUnit import ControlUnit
from DataMemory import DataMemory
from instructionMemory import instructionMemory
from PC import PC
from registerFile import registerFile
from SignZeroExtend import SignZeroExtend


@block
def singleCyleCpu():  #clk, Reset
    opCode = Signal(intbv(0)[6:])
    signal_32bit = [Signal(intbv(0)[32:]) for i in range(4)]
    Out1, Out2, curPC, Result = signal_32bit

    ALUOp = Signal(intbv(0)[3:])
    ExtOut = Signal(intbv(0)[32:])
    DMOut = Signal(intbv(0)[32:])
    immediate = Signal(intbv(0)[16:])

    signal_5bit = [Signal(intbv(0)[5:]) for i in range(3)]
    rs, rt, rd = signal_5bit

    signal_1bit = [Signal(intbv(0)[1:]) for i in range(12)]
    Reset, clk, zero, PCWre, PCSrc, ALUSrcB, ALUM2Reg,\
         RegWre, InsMemRW, DataMemRW, ExtSel, RegOut = signal_1bit

    clk = Signal(intbv(0)[1:])
    # zero = Signal(intbv(1)[1:])

    clock = Clock(clk)
    alu = ALU(Out1, Out2, ExtOut, ALUSrcB, ALUOp, zero, Result)
    pc = PC(clk, Reset, PCWre, PCSrc, immediate, curPC)
    control = ControlUnit(opCode, zero, PCWre, ALUSrcB, ALUM2Reg, RegWre,
                          InsMemRW, DataMemRW, ExtSel, PCSrc, RegOut, ALUOp)
    datamemory = DataMemory(Result, Out2, DataMemRW, DMOut)
    ins = instructionMemory(curPC, InsMemRW, opCode, rs, rt, rd, immediate)
    registerfile = registerFile(clk, RegWre, RegOut, rs, rt, rd, ALUM2Reg,
                                Result, DMOut, Out1, Out2)
    ext = SignZeroExtend(immediate, ExtSel, ExtOut)

    @instance
    def stimulus():
        Reset.next = 1
        while True:
            yield delay(1)
            print('-----------------------------------------------------------')
            print('clk:' + str(clk), 'opcode:' + '{0:06b}'.format(int(opCode)),
                  'Out1:' + str(Out1), 'Out2:' + str(Out2),
                  'curPc:' + str(curPC), 'Result:' + str(Result))
            print('-----------------------------------------------------------\n')
    return instances()


def main():
    t = singleCyleCpu()
    t.run_sim(4)


if __name__ == '__main__':
    main()
