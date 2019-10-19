from myhdl import *


@block
def DataMemory(DAddr, DataIn, DataMemRW, DataOut):

    memory = [Signal(intbv(0)[32:] for i in range(32)]
    @always(DataMemRw)
    def read_data():
        if DataMemRw == 0:
            DataOut.next = memory[DAddr]
    

    @always(DataMemRW, DAddr, DataIn)
    def write_data():
        if DataMemRW:
            memory[DAddr].next = DataIn

    return read_data, write_data

@block
def test():
    # TODO