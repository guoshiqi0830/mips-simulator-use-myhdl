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
def singleCyleCpu(clk, Reset, opCode, Out1, Out2, curPC, Result):
    opCode = Signal(intbv(0)[6:])
    signal_32bit = [Signal(intbv(0)[32:]) for i in range(4)]
    Out1, Out2, curPC, Result = signal_32bit

    ALUOp = Signal(intbv(0)[3:])
    ExtOut = Signal(intbv(0)[32:])
    DMOut = Signal(intbv(0)[32:])
    immediate = Signal(intbv(0)[16:])

    signal_5bit = [Signal(intbv(0)[5:]) for i in range(3)]
    rs, rt, rd = signal_5bit

    signal_1bit = [Signal(intbv(0)[1:]) for i in range(10)]
    zero, PCWre, PCSrc, ALUSrcB, ALUM2Reg, RegWre, InsMemRW, DataMemRW, ExtSel, RegOut = signal_1bit
    
    # 简化的ALU，没有引入立即数扩展功能
    alu = ALU(ALUOp, Out1, Out2, result, zero)
    clock = Clock(clk)
    pc = PC(clk, Reset, PCWre, PCSrc, immediate, curPC)
    control = ControlUnit(opCode, zero, PCWre, ALUSrcB, ALUM2Reg, RegWre, InsMemRW,
                DataMemRW, ExtSel, PCSrc, RegOut, ALUOp)
    datamemory = dataMemory(Result, Out2, DataMemRW, DMOut)
    ins = instructionMemory(curPC, InsMemRW, opCode, rs, rt, rd, immediate)
    registerfile = registerFile(clk, RegWre, RegOut, rs, rt, rd, ALUM2Reg, 
                 Result, DMOut, Out1, Out2)
    # 并没有使用到立即数扩展这个模块
    ext = SignZeroExtend(immediate,ExtSel, ExtOut)
    
    # @instance
    # def stimulus():
    #     Reset.next = 1
    #     while True:
    #         for ops in []:
    #             opCode.next = ops
    #             print(Out1, Out2, curPC, Result)
    #             yield delay(1)
