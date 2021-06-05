#“On my honor, I have neither given nor received unauthorized aid on this assignment”
#This is a step-by-step PetriNet simulator for a MIPS processor developed using python

import os

#Initializing the required vaiables
INM = [] #Instruction Memory - List type
RGF = {} #Register File - Dictionary type
DAM = {} #Data memory - Dictionary type
INB = [] #Instruction Buffer  - List type
AIB = [] #Arithmetic Instruction Buffer  - List type
LIB = [] #Load Instruction Buffer - List type
ADB = [] #Address Buffer - List type
REB = [] #Result Buffer  - List type
arithmetic_operands =["ADD", "SUB", "AND", "OR"] #list of different logical oparands used in this project

#This is a MIPS Processor simulation block of type CLASS
class  mipsPocessorSimulation:
    #Load instruction method which takes the Instructions.txt as input and it returns the INM list in specific format
    def load_instructions(self,filepath):
        with open(filepath, "r") as f:
            [INM.append(l.strip("< >\n").split(',')) for l in f]
        return INM

    # Load register method which takes the register.txt as input and it returns the RGF as a list in specific format
    def load_register(self, filepath):
        with open(filepath, "r") as f:
            for l in f:
                (k, v) = l.strip("<>\n").split(',')
                RGF[k] = v         #assigining the key value pairs to RGF dictionary
        return RGF

    # Load datamemory method which takes the datamemory.txt as input and it returns the DAM as a list in specific format
    def load_datamemory(self, filepath):
        with open(filepath, "r") as f:
            for l in f:
                (k, v) = l.strip("<>\n").split(',')
                DAM[k] = v
        return DAM

    #Write methos preforms Write transaction when there is a value in REB
    def write(self):
        if REB:
            RGF[REB[0]] = str(REB[1])
            REB.pop(0) #removing first element address
            REB.pop(0) #removing first element value

    #Decode method performs the decoding instructuons for INM and RGF and creates INB by replacing the first and second operands
    def decode(self):
        if INM:
            if INM[0]:
                INB.extend([INM[0][0],INM[0][1],RGF[INM[0][2]],RGF[INM[0][3]]])
            INM.pop(0)
    #INBstate method to check for the the type of instruction(Logical or load) and assign to AIB or LIB and clears of the INB
    def inb_state(self):
        if INB:
            if INB[0] in arithmetic_operands:
                AIB.extend(INB)
                INB.clear()
            elif INB[0] == "LD":
                LIB.extend(INB)
                INB.clear()
    #adder methos perfoms the ADDER task , adds the oprands in the LIB. Clears the LIB at the end
    def adder(self):
        if LIB:
            ADB.extend([LIB[1], int(LIB[2]) + int(LIB[3])])
            LIB.clear()

    #load methos will write the content to the REB if ADB or AIB has the values in it by performing the corresponding logical operation. clears ADB and ADB at the end
    def load(self):
        if ADB:
            REB.extend([ADB[0],DAM[str(ADB[1])]])
            ADB.clear()
        if AIB:
            if AIB[0] == arithmetic_operands[0]:
                REB.extend([AIB[1],int(AIB[2])+int(AIB[3])])
            if AIB[0] == arithmetic_operands[1]:
                REB.extend([AIB[1], int(AIB[2]) - int(AIB[3])])
            if AIB[0] == arithmetic_operands[2]:
                REB.extend([AIB[1], int(AIB[2]) & int(AIB[3])])
            if AIB[0] == arithmetic_operands[3]:
                REB.extend([AIB[1], int(AIB[2]) | int(AIB[3])])
            AIB.clear()

    #Method to convert the INM list to INM string format
    def rebuilt_inm(self):
        str1 = ""
        if INM:
            for i in range(len(INM)):
                str1 += "<"+ str(INM[i][0])+","+str(INM[i][1])+","+str(INM[i][2])+","+str(INM[i][3])+">"
                if i < (int((len(INM))) -1):
                    str1 += ","
            return str1
        else:
            return str1

    # Method to convert the INB list to INB string format
    def rebuilt_inb(self):
        str1 = ""
        if INB:
            str1 = "<" + str(INB[0]) +"," + str(INB[1]) +","  + str(INB[2]) +"," + str(INB[3]) +">"
            return str1
        else:
            return str1

    # Method to convert the AIB list to AIB string format
    def rebuilt_aib(self):
        str1=""
        if AIB:
            str1 = "<" + str(AIB[0]) +"," + str(AIB[1]) +"," + str(AIB[2]) +"," + str(AIB[3]) +">"
            return str1
        else:
            return str1

    # Method to convert the LIB list to LIB string format
    def rebuilt_lib(self):
        str1 = ""
        if LIB:
            str1 = "<" + str(LIB[0]) + "," + str(LIB[1]) + "," + str(LIB[2]) + "," + str(LIB[3]) + ">"
            return str1
        else:
            return str1

    # Method to convert the ADB list to ADB string format
    def rebuilt_adb(self):
        str1 = ""
        if ADB:
            #print("ADB=",ADB)
            str1 = "<" + str(ADB[0]) + "," + str(ADB[1]) + ">"
            return str1
        else:
            return str1

    # Method to convert the REB list to REB string format
    def rebuilt_reb(self):
        str1 = ""
        if REB:
            if len(REB) == 2:
                str1 = "<" + str(REB[0]) + "," + str(REB[1]) +">"
                return str1
            elif len(REB) == 4:
                str1 = "<" + str(REB[0]) + "," + str(REB[1]) + ">,""<" + str(REB[2]) + "," + str(REB[3]) + ">"
                return str1
        else:
            return str1

    # Method to convert the RGF Dictonary to RGF string format
    def rebuilt_rgf(self):
        str1=""
        if RGF:
            str1 = str(RGF)
            str1 = str1.replace("', '", '>,<')
            str1 = str1.replace("': '", ",")
            str1 = str1.replace("{'", "<")
            str1 = str1.replace("'}", ">")
            return str1

    # Method to convert the DAM dictionary to DAM string format
    def rebuilt_dam(self):
        str1=""
        if DAM:
            str1 = str(DAM)
            str1 = str1.replace("', '", '>,<')
            str1 = str1.replace("': '", ",")
            str1 = str1.replace("{'", "<")
            str1 = str1.replace("'}", ">")
            return str1

Psim = mipsPocessorSimulation() #object creation the Processor simulation class
Psim.load_instructions("instructions.txt") #passing instructions.txt
Psim.load_register("registers.txt") #passing registers.txt
Psim.load_datamemory("datamemory.txt") #passing datamemory.txt

count = 0 #initializing the count to 0 for loopin through the simulation

ofile = open("simulation.txt", "w") #opening simulation.txt for saving the output
#Out file format as below
ofile.write("STEP " + str(count) + ":\n")
ofile.write("INM:" + str(Psim.rebuilt_inm()) + "\n")
ofile.write("INB:" + str(Psim.rebuilt_inb()) + "\n")
ofile.write("AIB:" + str(Psim.rebuilt_aib()) + "\n")
ofile.write("LIB:" + str(Psim.rebuilt_lib()) + "\n")
ofile.write("ADB:" + str(Psim.rebuilt_adb()) + "\n")
ofile.write("REB:" + str(Psim.rebuilt_reb()) + "\n")
ofile.write("RGF:" + str(Psim.rebuilt_rgf()) + "\n")
ofile.write("DAM:" + str(Psim.rebuilt_dam()) + "\n\n")

#while loop to process the simulation of processor until there is no instructions to process in the intruction set
while(INM or INB or AIB or LIB or ADB or REB):

    count += 1
    Psim.write()
    Psim.load()
    Psim.adder()
    Psim.inb_state()
    Psim.decode()
    ofile.write("STEP " + str(count) + ":\n")
    ofile.write("INM:" + str(Psim.rebuilt_inm()) + "\n")
    ofile.write("INB:" + str(Psim.rebuilt_inb()) + "\n")
    ofile.write("AIB:" + str(Psim.rebuilt_aib()) + "\n")
    ofile.write("LIB:" + str(Psim.rebuilt_lib()) + "\n")
    ofile.write("ADB:" + str(Psim.rebuilt_adb()) + "\n")
    ofile.write("REB:" + str(Psim.rebuilt_reb()) + "\n")
    ofile.write("RGF:" + str(Psim.rebuilt_rgf()) + "\n")
    ofile.write("DAM:" + str(Psim.rebuilt_dam()) + "\n\n")

remove_chars = len(os.linesep) #On Linux and MacOS, the -1 is correct, but on Windows it needs to be -2. A more Pythonic method of determining which is to check os.linesep.
ofile.truncate(ofile.tell()- remove_chars) # At the end of the file(before closing) truncating the extra new lines character.
ofile.close()# closing the file in the end