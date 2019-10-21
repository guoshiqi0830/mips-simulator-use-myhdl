from myhdl import *


@block
def instructionMemory(pc, InsMemRW, op, rs, rt, rd, immediate):
    mem = [Signal(intbv(0)[32:]) for i in range(16)]
    mem[0] = intbv(0)[32:]

    # lw $2 0($1)
    # get datamem[2] to reg[2]
    mem[1] = intbv('100111' + '00000' + '00010' + '0000000000000011')[32:]

    # addi $1 $0 3
    # reg[1] = 3
    mem[3] = intbv('000001' + '00000' + '00001' + '0000000000000011')[32:]

    # lw $3 0($1)
    # get datamem[3] to reg[3]
    mem[4] = intbv('100111' + '00001' + '00011' + '0000000000000000')[32:]

    # add $4 $2 $3
    mem[5] = intbv('000000' + '00010' + '00011' + '0010000000000000')[32:]

    @always_comb
    def logic():
        print('-> Enter insMem')
        if InsMemRW == 0:
            ins = mem[pc // 4]
            op.next = ins[32:26]
            rs.next = ins[26:21]
            rt.next = ins[21:16]
            rd.next = ins[16:11]
            immediate.next = ins[16:]
            print('pc:' + str(pc),
                  'ins:' + '{0:032b}'.format(int(str(ins[32:]), 16)))
            print('op:' + '{0:06b}'.format(int(str(ins[32:26]), 16)),
                  'rs:' + '{0:05b}'.format(int(str(ins[26:21]), 16)),
                  'rt:' + '{0:05b}'.format(int(str(ins[21:16]), 16)),
                  'rd:' + '{0:05b}'.format(int(str(ins[16:11]), 16)),
                  'immediate:' + '{0:016b}'.format(int(str(ins[16:]), 16)))
        print('<- Exit insMem\n')

    return logic


@block
def test():
    pc = Signal(intbv(0)[32:])
    InsMemRW = Signal(intbv(0)[1:])
    op = Signal(intbv(0)[6:])
    signal_5bit = [Signal(intbv(0)[5:]) for i in range(3)]
    rs, rt, rd = signal_5bit
    immediate = Signal(intbv(0)[16:])

    ins = instructionMemory(pc, InsMemRW, op, rs, rt, rd, immediate)

    @instance
    def stimulus():
        for i in range(1):
            pc.next = intbv(i * 4)
            yield delay(10)
            print(pc.next, '{0:06b}'.format(int(op)),
                  '{0:05b}'.format(int(rs)), '{0:05b}'.format(int(rt)),
                  '{0:05b}'.format(int(rd)), '{0:016b}'.format(int(immediate)))

    return instances()


def main():
    t = test()
    t.run_sim()


if __name__ == '__main__':
    main()