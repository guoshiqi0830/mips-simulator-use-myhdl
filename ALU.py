from myhdl import *


@block
def ALU(ReadData1, ReadData2, inExt, ALUSrcB, ALUOp, zero, result,
        DEBUG=False):
    '''
    算术运算单元
    @param Data1 操作数1 寄存器文件单元
    @param Data2 操作数2 寄存器文件单元
    @param intExt 操作数2 拓展单元
    @param ALUSrcB 控制单元控制信号。0,第二操作数为ReadData2; 否则为intExt;
    @param ALUOp 操作标志
    @param zero 输出 控制信号。result=0，zerro=1；否则为0
    @param result 结果=0,zero=1; 否则zero为0；
    '''

    @always(ReadData1, ReadData2, inExt, ALUSrcB, ALUOp)
    def logic():
        if DEBUG:
            print('->Enter ALU')
            print('ReadData1:' + str(ReadData1), 'ReadData2:' + str(ReadData2),
                  'inExt:' + str(inExt), 'ALUSrcB:' + str(ALUSrcB),
                  'ALUOp:' + str(ALUOp))

        A = ReadData1
        # 根据ALUSrcB选择数据来源，0则从寄存器取，1则从扩展单元取
        if ALUSrcB == 0:
            B = ReadData2
        else:
            B = inExt

        if ALUOp == intbv('000'):
            result.next = A + B
        elif ALUOp == intbv('001'):
            result.next = A - B
        elif ALUOp == intbv('010'):
            result.next = B - A
        elif ALUOp == intbv('011'):
            result.next = A | B
        elif ALUOp == intbv('100'):
            result.next = A & B
        elif ALUOp == intbv('101'):
            result.next = (~A) & B
        elif ALUOp == intbv('110'):
            result.next = A ^ B
        elif ALUOp == intbv('111'):
            # result.next = A ^ ~B
            if A[31] ^ B[31]:
                if A[31]:
                    result.next = 1
                else:
                    result.next = 0
            else:
                if A < B:
                    result.next = 1
                else:
                    result.next = 0


        if DEBUG:
            print('<-Exit ALU\n')

    @always_comb
    def zero_detector():
        if result == 0:
            zero.next = 1
        else:
            zero.next = 0

    return logic, zero_detector

@block
def test1():
    readData1 = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    readData2 = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    inExt = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    aluSrcB = Signal(intbv(0, 0, 1));
    aluOp = Signal(intbv(0)[3:]);
    zero = Signal(0)
    result = Signal(intbv(0, min=-(2 ** 31), max=2 ** 31 - 1))
    debug = True

    alu = ALU(readData1, readData2, inExt, aluSrcB, aluOp, zero, result, debug)
    @instance
    def stimulus():
        readData1.next = int('111', 2)
        for aluop in ('000', '001'):
            aluOp.next = intbv(aluop)

            yield delay(10)
            print(aluop)
    return instances()

@block
def test():
    ALUOp = Signal(intbv(0)[3:])
    A = Signal(intbv(0, min=-(2**31), max=2**31 - 1))
    B = Signal(intbv(0, min=-(2**31), max=2**31 - 1))
    result = Signal(intbv(0, min=-(2**31), max=2**31 - 1))
    zero = Signal(0)

    alu = ALU(ALUOp, A, B, result, zero)

    @instance
    def stimulus():
        A.next = int('111', 2)
        B.next = int('010', 2)
        for aluop in ('000', '001', '010', '011', '100', '101', '110', '111'):
            ALUOp.next = intbv(aluop)

            yield delay(10)
            print(aluop)
            print(A, B, result, zero)

    return instances()


def main():
    t = test1()
    t.run_sim()


if __name__ == '__main__':
    main()