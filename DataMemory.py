from myhdl import *


@block
def DataMemory(DAddr, DataIn, DataMemRW, DataOut):

    memory = [Signal(intbv(0)[32:]) for i in range(32)]
    memory[0] = intbv(0x00000009)[32:]
    memory[1] = intbv(0x00000008)[32:]
    memory[2] = intbv(0x00000007)[32:]
    memory[3] = intbv(0x00000006)[32:]

    @always(DataMemRW, DAddr)
    def read_data():
        print('-> Enter dataMem read data')
        print('DAddr:' + str(DAddr), 'DataIn:' + str(DataIn),
              'DataMemRW:' + str(DataMemRW))
        if DataMemRW == 0:
            DataOut.next = memory[DAddr]
            print('read addr:' + str(DAddr), 'data:' + str(memory[DAddr]))
        print('<- Exit dataMem read data\n')

    @always(DataMemRW) # , DAddr, DataIn
    def write_data():
        print('-> Enter dataMem write data')
        print('DAddr:' + str(DAddr), 'DataIn:' + str(DataIn),
              'DataMemRW:' + str(DataMemRW))
        if DataMemRW:
            memory[DAddr].next = DataIn
            print('write addr:' + str(DAddr), 'data:' + str(DataIn))
        print('<- Exit dataMem write data\n')

    return read_data, write_data
