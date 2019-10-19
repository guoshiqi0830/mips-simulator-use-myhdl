from myhdl import *


@block
def instructionMemory(pc, InsMemRW, op, rs, rt, rd, immediate):
    mem = [Signal(intbv(0)[32:] for i in range(16)]
    @always_comb
    def logic():
        mem[0].next = 0x00000000
        mem[1].next = 0x04010000
        mem[2].next = 0x4002000C
        mem[3].next = 0x00221800
        mem[4].next = 0x08412000
        mem[5].next = 0x44222800
        mem[6].next = 0x48223000
        mem[7].next = 0xC0220004
        mem[8].next = 0x80203800
        mem[9].next = 0x98E10001
        mem[10].next = 0x9C220000
        mem[11].next = 0xC047FFFB
        mem[12].next = 0xFC000000
        mem[13].next = 0x00000000
        mem[14].next = 0x00000000
        mem[15].next = 0x00000000
    return logic
