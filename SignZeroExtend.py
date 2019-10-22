from myhdl import *


@block
def SignZeroExtend(immediate, ExtSel, out, DEBUG=False):
    @always(immediate, ExtSel)
    def logic():
        if DEBUG:
            print('-> Enter SignZeroExtend')
            print('immediate:' + str(immediate), 'ExtSel:' + str(ExtSel))

        _out = intbv(0)[32:]
        _out[16:] = immediate
        # 立即数高16位扩展，立即数最高位为1则扩展16个1，否则扩展16个0
        _out[32:16] = (intbv(0xffff)[16:] if immediate[15] else
                       intbv(0)[16:]) if ExtSel else intbv(0)[16:]
        out.next = _out

        if DEBUG:
            print('out:' + str(_out))
            print('<- Exit SignZeroExtend\n')

    return logic


@block
def test():
    immediate = Signal(intbv(0x0fff)[16:])
    ExtSel = Signal(intbv(1)[1:])
    out = Signal(intbv(0)[32:])

    sze = SignZeroExtend(immediate, ExtSel, out)

    @instance
    def Stimulus():
        while True:
            yield delay(1)
            print(immediate, ExtSel, out)

    return instances()


def main():
    t = test()
    t.run_sim(1)


if __name__ == '__main__':
    main()
