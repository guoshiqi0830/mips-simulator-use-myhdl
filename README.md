# 基于python myhdl编写的MIPS模拟器

代码地址：https://github.com/Guoshiqi0830/mips-simulator-use-myhdl

## 整体结构
整体结构参照doc文件夹中实验文档的verilog代码。  
共分为9个模块，分别为：  
ALU  
Clock  
ControlUnit  
DataMemory  
instructionMemory  
PC  
registerFile  
SignZeroExtend  
SingleCycleCPU

## 运行
1. 在singleCycleCPU.py的main函数中传入program文件名作为参数即可运行。  
2. 每个模块的最后一个参数为DEBUG，在顶层模块中传入True可打印运行过程。  
3. DataMemory 中硬编码了内存数据，可在其中更改。  

## 更改
相比实验文档改写了少部分逻辑, 改写的内容有：  
1. 增加了时钟驱动模块  
2. ControlUnit中 DataMemRW 改为 DataMemR 和 DataMemW 两个信号。  
3. ALU中 ALUOp 为111时的操作改为了判断小于。  

## 参考
python myhdl的写法可以参考doc中的官方文档myhdl.pdf。   
编码过程中参考了https://github.com/mgaitan/pymips
