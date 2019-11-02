# 基于python myhdl编写的MIPS单周期模拟器

代码地址：https://github.com/Guoshiqi0830/mips-simulator-use-myhdl

## 环境需求
python  
myhdl

## 整体结构
整体结构参照doc文件夹中实验文档的verilog代码。  
共分为9个模块，分别为：  
ALU, Clock, ControlUnit, DataMemory, instructionMemory, PC, registerFile, SignZeroExtend, SingleCycleCPU  

## 模块详细说明
1. ALU：  
根据ALUop 对输入的两数进行操作并输出。
2. Clock:  
时钟驱动，0 1 交替输出信号。
3. ControlUnit:  
根据instructionMemory解析出的操作码发出控制信号，具体信号含义详见代码注释。
4. DataMemory:  
存储、读取内存中的数据，使用数组实现。
5. PC:  
控制读取下一条指令。
6. registerFile:  
读取、写入寄存器，寄存器使用数组实现。
7. SignZeroExtend:  
将扩展立即数至32位。
8. SingleCycleCPU:  
顶层模块，将其余各模块连接起来。

## 运行
1. 在singleCycleCPU.py的main函数中传入program文件名作为参数即可运行，program 已加入的程序有 add and lessthan lessthan0。  
2. 每个模块的最后一个参数为DEBUG，在顶层模块中传入True可打印运行过程。  
3. DataMemory 中硬编码了内存数据，可在其中更改。

## 更改
相比实验文档改写了少部分逻辑, 改写的内容有：  
1. 增加了时钟驱动模块  
2. ControlUnit中 DataMemRW 改为 DataMemR 和 DataMemW 两个信号。  
3. ALU中 ALUOp 为111时的操作改为了判断小于。  
4. registerFile 中改为仅在时钟下降沿写入寄存器。

## 可改进的地方
1. R型指令的func并没有引入。
2. 多路选择器写在了具体模块中，并不直观，可分离出来。
3. 寄存器的类型没有细分。

## 参考
python myhdl的写法可以参考doc中的官方文档myhdl.pdf。   
编码过程中参考了https://github.com/mgaitan/pymips
