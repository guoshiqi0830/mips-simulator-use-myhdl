from myhdl import *
from Clock import Clock


@block
def PC(clk, Reset, PCWre, PCSrc, immediate, Address):
    @always(clk.posedge, Reset.negedge)
    def logic():
        print('-> Enter PC')
        print('Address:' + str(Address), 'PCWre:' + str(PCWre),
              'PCSrc:' + str(PCSrc))
        if Reset == 0:
            Address.next = 0
        elif PCWre:
            if PCSrc:
                Address.next = Address + 4 + immediate * 4
            else:
                Address.next = Address + 4
        print('<- Exit PC\n')

    return logic


@block
def test():
    clk = Signal(intbv(0)[1:])
    Reset = Signal(intbv(1)[1:])
    PCWre = Signal(intbv(1)[1:])
    PCSrc = Signal(intbv(1)[1:])
    Address = Signal(intbv(0)[32:])
    immediate = Signal(intbv(0)[32:])

    clock = Clock(clk)
    pc = PC(clk, Reset, PCWre, PCSrc, immediate, Address)

    @instance
    def stimulus():
        Address.next = int('1000', 2)
        immediate.next = int('0100', 2)
        while True:
            yield delay(1)
            print(clk, Reset, PCWre, PCSrc, immediate, int(Address))

    return instances()


def main():
    t = test()
    t.run_sim(10)


if __name__ == '__main__':
    main()
