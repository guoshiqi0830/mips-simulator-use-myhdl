from myhdl import *


@block
def instructionMemory(pc, InsMemRW, op, rs, rt, rd, immediate):
    mem = [Signal(intbv(0)[32:]) for i in range(16)]
    mem[0] = intbv(0x00000000)[32:]
    mem[1] = intbv(0b10011100001000010000000000000000)[32:]
    mem[2] = intbv(0b10011100010000100000000000000001)[32:]
    # mem[1] = intbv(0b10011100001)[32:]
    # mem[0] = intbv(0x00000000)[32:]
    # mem[1] = intbv(0x04010000)[32:]
    # mem[2] = intbv(0x4002000C)[32:]
    # mem[3] = intbv(0x00221800)[32:]
    # mem[4] = intbv(0x08412000)[32:]
    # mem[5] = intbv(0x44222800)[32:]
    # mem[6] = intbv(0x48223000)[32:]
    # mem[7] = intbv(0xC0220004)[32:]
    # mem[8] = intbv(0x80203800)[32:]
    # mem[9] = intbv(0x98E10001)[32:]
    # mem[10] = intbv(0x9C220000)[32:]
    # mem[11] = intbv(0xC047FFFB)[32:]
    # mem[12] = intbv(0xFC000000)[32:]
    # mem[13] = intbv(0x00000000)[32:]
    # mem[14] = intbv(0x00000000)[32:]
    # mem[15] = intbv(0x00000000)[32:]

    @always_comb
    def logic():
        print('Enter insMem')
        print('pc：' + str(pc))
        if InsMemRW == 0:
            code = mem[pc // 4]
            op.next = code[32:26]
            rs.next = code[26:21]
            rt.next = code[21:16]
            rd.next = code[16:11]
            immediate.next = code[16:]
        print('Exit insMem\n')
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