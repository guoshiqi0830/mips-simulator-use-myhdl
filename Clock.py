from myhdl import *

@block
def Clock(clk, period=1):
    '''
    时钟驱动
    @param clk: 时钟信号
    '''
    halfPeriod = delay(period)

    @always(halfPeriod)
    def drive_clock():
        clk.next = not clk

    return drive_clock

@block
def test():
    clk = Signal(0)
    clock = Clock(clk)

    @instance
    def Stimulus():
        while True:
            yield delay(1)
            print(int(clk))
    
    return instances()


def main():
    t = test()
    t.run_sim(2)


if __name__ == '__main__':
    main()

