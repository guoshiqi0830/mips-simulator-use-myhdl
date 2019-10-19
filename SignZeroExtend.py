from myhdl import *

@block
def SignZeroExtend(immediate, ExtSel, out):
    @always_comb
    def logic():
        _out = intbv(0)[32:]
        _out[16:] = immediate
        _out[32:16] = (intbv(0xffff)[16:] if immediate[15] else intbv(0)[16:]) if ExtSel else intbv(0)[16:]
        out.next = _out
    
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
