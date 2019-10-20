from myhdl import *


@block
def DataMemory(DAddr, DataIn, DataMemRW, DataOut):

    memory = [Signal(intbv(0)[32:]) for i in range(32)]
    memory[0] = intbv(0x00000008)[32:]
    memory[1] = intbv(0x00000007)[32:]
    memory[2] = intbv(0x00000003)[32:]
    memory[3] = intbv(0x00000004)[32:]
    @always_comb
    def read_data():
        print('Enter dataMem read data')
        print(DAddr, DataIn, DataMemRW)
        if DataMemRW == 0:
            DataOut.next = memory[DAddr]
        print('Exit dataMem read data\n')

    @always(DataMemRW, DAddr, DataIn)
    def write_data():
        print('Enter dataMem write data')
        print(DAddr, DataIn, DataMemRW)
        if DataMemRW:
            memory[DAddr].next = DataIn
        print('Exit dataMem write data\n')
    return read_data, write_data
