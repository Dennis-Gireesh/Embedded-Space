# Petrinet simulation for a MIPS processor

> MIPS Datapath figure.\
![image](https://user-images.githubusercontent.com/45356812/120899806-872ae600-c5ff-11eb-804c-603b28762798.png) \
\
This petrinet model has three important places (instruction memory, register file, and data memory) and eight transitions.\

\
> THREE IMPORTANT PLACES
**1. Instruction Memory (INM):**
The processor to be simulated only supports five types of instructions: add (ADD), subtract (SUB), logical 
and (AND), logical or (OR), and load (LD). At a time step, the place denoted as Instruction Memory (INM) 
can have up to 16 instruction tokens. This is shown as Ii in Figure 1. We will provide an input file 
(instructions.txt) with up to 16 instruction tokens. It supports the following instruction format. Please note 
that both source operands are always registers.
<Opcode>, <Destination Register>, <First Source Operand>, <Second Source Operand>
Sample instruction tokens and equivalent functionality are shown below:
<ADD, R1, R2, R3> ➔ R1 = R2 + R3
<SUB, R1, R2, R3> ➔ R1 = R2 – R3
<AND, R1, R2, R3> ➔ R1 = R2 & R3
<OR, R1, R2, R3> ➔ R1 = R2 | R3
<LD, R1, R2, R3> ➔ R1 = DataMemory[R2+R3]
**2. Register File (RGF):**
This processor supports up to 8 registers (R0 through R7). At a time step it can have up to 8 tokens. The 
token format is <registername, registervalue>, e.g., <R1, 5>. This is shown as Xi in Figure 1. We will 
provide an input file (registers.txt) with 8 register tokens that you can use to initialize the registers. You can 
assume that the content of a register can vary between 0 - 63.
**3. Data Memory (DAM):**
This processor supports up to 8 locations (0 – 7) in the data memory. At a time step it can have up to 8 tokens. 
The token format is <address, value>, e.g., <6, 5> implies that memory address 6 has value 5. This is shown 
as Di in Figure 1. We will provide an input file (datamemory.txt) with 8 data tokens that you can use to 
initialize the data memory locations. You can assume that the content of a data memory location can vary 
between 0 - 63\
  \
  \
> EIGHT TRANSITIONS
**1. READ:**
The READ transition is a slight deviation from traditional Petri net semantics since it does not have any 
direct access to instruction tokens. Assume that it knows the top (in-order) instruction in the Instruction
Memory (INM). It checks for the availability of the source operands in the Register File (RGF) for the top 
instruction token and passes them to Instruction Buffer (INB) by replacing the source operands with the 
respective values. For example, if the top instruction token in INM is <ADD, R1, R2, R3> and there are two 
tokens in RGF as <R2,5> and <R3,7>, then the instruction token in INB would be <ADD,R1,5,7> once both 
READ and DECODE transitions are activated. Both READ and DECODE transitions are executed together. 
Please note that when READ consumes two register tokens, it also returns them to RGF in the same time step
(no change in RGF due to READ).\
 2. DECODE:
The DECODE transition consumes the top (in-order) instruction (one token) from INM and updates the 
values of the source registers with the values from RGF (with the help of READ transition, as described 
above), and places the modified instruction token in INB.
3. ISSUE1:
ISSUE1 transition consumes one arithmetic/logical (ADD, SUB, AND, OR) instruction token (if any) from 
INB and places it in the Arithmetic Instruction Buffer (AIB).
4. ISSUE2:
ISSUE2 transition consumes one load (LD) instruction token (if any) from INB and places it in the Load 
Instruction Buffer (LIB).
5. Arithmetic Logic Unit (ALU)
ALU transition performs arithmetic/logical computations as per the instruction token from AIB, and places 
the result in the result buffer (REB). The format of the token in result buffer is same as a token in RGF i.e., 
<destination-register-name, value>.
6. Address Calculation (ADDR)
ADDR transition performs effective (data memory) address calculation for the load instruction by adding the 
contents of two source registers. It produces a token as <destination-register-name, data memory address> 
and places it in the address buffer (ADB).
7. LOAD:
The LOAD transition consumes a token from ADB and gets the data from the data memory for the 
corresponding address. Assume that you will always have the data for the respective address in the data 
memory in the same time step. It places the data value (result of load) in the result buffer (REB). The format 
of the token in result buffer is same as a token in RGF i.e., <destination-register-name, data value>.
8. WRITE
Transfers the result (one token) from the Result Buffer (REB) to the register file (RGF). If there are more 
than one token in REB in a time step, the WRITE transition writes the token that belongs to the in-order first 
instruction.

