from myhdl import *


@block
def ALU(ReadData1, ReadData2, inExt, ALUSrcB, ALUOp, zero, result,
        DEBUG=False):
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
def test():
    ALUOp = Signal(intbv(0)[3:])
    ReadData1 = Signal(intbv(0, min=-(2**31), max=2**31 - 1))
    ReadData2 = Signal(intbv(0, min=-(2**31), max=2**31 - 1))
    result = Signal(intbv(0, min=-(2**31), max=2**31 - 1))
    zero = Signal(0)
    inExt = Signal(0)
    ALUSrcB = Signal(0)

    alu = ALU(ReadData1, ReadData2, inExt, ALUSrcB, ALUOp, zero, result)

    @instance
    def stimulus():
        ReadData1.next = int('111', 2)
        ReadData2.next = int('010', 2)
        for aluop in ('000', '001', '010', '011', '100', '101', '110', '111'):
            ALUOp.next = intbv(aluop)

            yield delay(10)
            print('aluop:', aluop)
            print('A:', ReadData1, 'B:', ReadData2, 'result:', result, 'zero:',
                  zero)

    return instances()


def main():
    t = test()
    t.run_sim()


if __name__ == '__main__':
    main()