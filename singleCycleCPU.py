from myhdl import *
from ALU import ALU
from Clock import Clock
from ControlUnit import ControlUnit
from DataMemory import DataMemory
from instructionMemory import instructionMemory
from PC import PC
from registerFile import registerFile
from SignZeroExtend import SignZeroExtend

import io
import re


@block
def singleCyleCpu(instructions):  #clk, Reset
    opCode = Signal(intbv(0)[6:])
    signal_32bit = [Signal(intbv(0)[32:]) for i in range(4)]
    Out1, Out2, curPC, Result = signal_32bit

    ALUOp = Signal(intbv(0)[3:])
    ExtOut = Signal(intbv(0)[32:])
    DMOut = Signal(intbv(0)[32:])
    immediate = Signal(intbv(0)[16:])

    signal_5bit = [Signal(intbv(0)[5:]) for i in range(3)]
    rs, rt, rd = signal_5bit

    signal_1bit = [Signal(intbv(0)[1:]) for i in range(13)]
    Reset, clk, zero, PCWre, PCSrc, ALUSrcB, ALUM2Reg,\
         RegWre, InsMemRW, DataMemR, DataMemW, ExtSel, RegOut = signal_1bit

    clk = Signal(intbv(1)[1:])

    clock = Clock(clk)
    alu = ALU(Out1, Out2, ExtOut, ALUSrcB, ALUOp, zero, Result, True)
    pc = PC(clk, Reset, PCWre, PCSrc, immediate, curPC, True)
    control = ControlUnit(opCode, zero, PCWre, ALUSrcB, ALUM2Reg, RegWre,
                          InsMemRW, DataMemR, DataMemW, ExtSel, PCSrc, RegOut,
                          ALUOp, True)
    datamemory = DataMemory(clk, Result, Out2, DataMemR, DataMemW, DMOut, True)
    insmem = instructionMemory(instructions, curPC, InsMemRW, opCode, rs, rt,
                               rd, immediate, True)
    registerfile = registerFile(clk, RegWre, RegOut, rs, rt, rd, ALUM2Reg,
                                Result, DMOut, Out1, Out2, True)
    ext = SignZeroExtend(immediate, ExtSel, ExtOut, True)

    @instance
    def stimulus():
        Reset.next = 1
        cycle = 1
        while True:
            yield delay(1)
            print('-' * 90)
            print('cycle:' + str(cycle), 'clk:' + str(clk),
                  'opcode:' + '{0:06b}'.format(int(opCode)),
                  'Out1:' + str(Out1), 'Out2:' + str(Out2),
                  'curPc:' + str(curPC), 'Result:' + str(Result))
            print('-' * 90, '\n')
            if not clk:
                cycle += 1

    return instances()


def load_program(program):
    '''
    从program文件夹中的文件中读取指令
    以文件名作为参数，不加后缀
    格式: 
    6位op  5位rs  5位rt  16位(rd)immediate ...
    '''
    ins = []
    cnt = 0
    with io.open('./program/' + program + '.txt') as f:
        for line in f:
            match = re.match('([0,1]{6}  [0,1]{5}  [0,1]{5}  [0,1]{16}).*',
                             line)
            if match:
                ins.append(match.group(1).replace(' ', ''))
                cnt += 1
    return ins, cnt


def main():
    program = 'lessthan0'

    instructions, cnt = load_program(program)
    t = singleCyleCpu(instructions)
    t.run_sim(2 * cnt)


if __name__ == '__main__':
    main()
