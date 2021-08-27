import sys
import matplotlib.pyplot as plt
from sys import stdin
reading = []

complete_input = sys.stdin.read()
temp=complete_input.splitlines()
for i in temp:
    reading.append(i)

while(len(reading) != 256):
    reading.append("0"*16)

def binary_converter(length, a): 
    a = int(a)
    ans = ""
    if(a == 0 or a == 1):
        return "0"*(length - 1) + str(a)
    while(a != 0 and a != 1):
        ans += str(a%2)
        a = a//2
    ans += str(a)
    ans = ans[::-1]
    n = len(ans)
    return "0"*(length-n) + ans

def integer_converter(a):
    ans = 0
    x = 0
    for i in a[::-1]:
        ans += (int(i)*(2**x))
        x += 1
    return ans

def unsigned_bitwise_not(a):
    a = binary_converter(16,a)

    ans = ""
    for i in a:
        if(i == "0"):
            ans += "1"
        else:
            ans += "0"
    return integer_converter(ans)

def unsigned_bitwise_and(a,b):
    c = binary_converter(16,a)
    d = binary_converter(16,b)
    ans = ""
    for i in range(16):
        if(c[i] == "1" and d[i] == "1"):
            ans += "1"
        else:
            ans += "0"
    return integer_converter(ans)

def unsigned_bitwise_xor(a,b):
    c = binary_converter(16,a)
    d = binary_converter(16,b)
    ans = ""
    for i in range(16):
        ans+=str(int(c[i])^int(d[i]))
    return integer_converter(ans)

def unsigned_bitwise_or(a,b):
    c = binary_converter(16,a)
    d = binary_converter(16,b)
    ans = ""
    for i in range(16):
        ans+=str(int(c[i]) | int(d[i]))
    return integer_converter(ans)

maxi = 0
PC = 0
cycle = 0
cycle_list = []
address_list = []
Register_list = [0,0,0,0,0,0,0,0] # [R0,R1,R2,R3,R4,R5,R6,FLAGS]

Register_code = {
    "000":0,
    "001":1,
    "010":2,
    "011":3,
    "100":4,
    "101":5,
    "110":6,
    "111":7
}



while(True):
    visited_address = []
    visited_address.append(PC)
    cycle_list.append(cycle)
    line = reading[PC]
    opcode = line[:5]

    if(opcode == "00000"):                          ## ADD Instruction :
        sys.stdout.write(binary_converter(8,PC)+" ")
        check = Register_list[Register_code[line[10:13]]] + Register_list[Register_code[line[13:]]]
        if(check>255): # Check for Overflow 
            Register_list[Register_code[line[7:10]]] = 0 ###Confirm--------
            flag_value = 8
            Register_list[7]= flag_value # Set Flag V as 1 
        else:
            Register_list[Register_code[line[7:10]]] = check
            Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1

    elif(opcode == "00001"):                        ## SUB Instruction :
        sys.stdout.write(binary_converter(8,PC)+" ")
        reg2 = Register_list[Register_code[line[10:13]]]
        reg3 = Register_list[Register_code[line[13:]]]
        if(reg3>reg2):                                                  # Subtraction Becomes Negative;No binary check required...
            Register_list[Register_code[line[7:10]]] = 0                # Zero given to R1 and Flag V is set afterwards 
            flag_value = 8
            Register_list[7]= flag_value                           # Set Flag V as 1 
        else:                                                           # Positive or Zero case
            check = Register_list[Register_code[line[10:13]]] - Register_list[Register_code[line[13:]]]
            if(check>255): # Check for Overflow 
                Register_list[Register_code[line[7:10]]] = 0 
                flag_value = 8
                Register_list[7]= flag_value # Set Flag V as 1 
            else:
                Register_list[Register_code[line[7:10]]] = check 
                Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1

    elif(opcode == "00010"):                      ## MOV Instruction (Mov R1 $2)
        sys.stdout.write(binary_converter(8,PC)+" ")
        new_Immdiate = integer_converter(line[8:]) #    ---->After 9?
        Register_list[Register_code[line[5:8]]] = new_Immdiate # In Decimal Form 
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "00011"):                      ## MOV Instruction (Mov R1 R2)
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[10:13]]] = Register_list[Register_code[line[13:]]]
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "00100"): # load
        sys.stdout.write(binary_converter(8,PC)+" ")
        value = integer_converter(reading[integer_converter(line[8:])])
        Register_list[Register_code[line[5:8]]] = value
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        visited_address.append(integer_converter(line[8:]))
    elif(opcode == "00101"): # store
        sys.stdout.write(binary_converter(8,PC)+" ")
        value = Register_list[Register_code[line[5:8]]]
        reading[integer_converter(line[8:])] = binary_converter(16,value)
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        visited_address.append(integer_converter(line[8:]))
    elif(opcode == "00110"):                      ## MUL Instruction :
        sys.stdout.write(binary_converter(8,PC)+" ")
        check = Register_list[Register_code[line[10:13]]] * Register_list[Register_code[line[13:]]]
        if(check>255): # Check for Overflow 
            Register_list[Register_code[line[7:10]]] = 0  ###Need to confirm 
            flag_value = 8
            Register_list[7]= flag_value # Set Flag V as 1 
        else:
            Register_list[Register_code[line[7:10]]] = check
            Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
    elif(opcode == "00111"):                     ## DIV Instruction   (div R0 R1)
        sys.stdout.write(binary_converter(8,PC)+" ")
        R1 = Register_list[Register_code[line[10:13]]]
        R2 = Register_list[Register_code[line[13:]]]
        Register_list[0] = R1//R2
        Register_list[1] = R1%R2
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01000"): #rightshift
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[5:8]]]=Register_list[Register_code[line[5:8]]]>>int([line[8:]],2)
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01001"): #leftshift
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[5:8]]]=Register_list[Register_code[line[5:8]]]<<int([line[8:]],2)
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01010"): #xor
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[7:10]]] = unsigned_bitwise_xor(Register_list[Register_code[line[10:13]]],Register_list[Register_code[line[13:]]])
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01011"): #or
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[7:10]]] = unsigned_bitwise_or(Register_list[Register_code[line[10:13]]],Register_list[Register_code[line[13:]]])
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01100"): 
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[7:10]]] = unsigned_bitwise_and(Register_list[Register_code[line[10:13]]],Register_list[Register_code[line[13:]]])
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01101"):
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[Register_code[line[10:13]]] = unsigned_bitwise_not(Register_list[Register_code[line[13:]]])
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
        
    elif(opcode == "01110"):
        sys.stdout.write(binary_converter(8,PC)+" ")

        if(Register_list[Register_code[line[10:13]]] == Register_list[Register_code[line[13:]]]):
            Register_list[7] = 1
        elif(Register_list[Register_code[line[10:13]]] > Register_list[Register_code[line[13:]]]):
            Register_list[7] = 2
        else:
            Register_list[7] = 4

        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        PC += 1
    elif(opcode == "01111"):
        sys.stdout.write(binary_converter(8,PC)+" ")

        PC = integer_converter(line[8:])
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        
    elif(opcode == "10000"):
        sys.stdout.write(binary_converter(8,PC)+" ")

        if(Register_list[7] == 4):
            PC = integer_converter(line[8:])
        else:
            PC += 1
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        
    elif(opcode == "10001"):
        sys.stdout.write(binary_converter(8,PC)+" ")

        if(Register_list[7] == 2):
            PC = integer_converter(line[8:])
        else:
            PC += 1
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        
    elif(opcode == "10010"):
        sys.stdout.write(binary_converter(8,PC)+" ")

        if(Register_list[7] == 1):
            PC = integer_converter(line[8:])
        else:
            PC += 1
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        
    elif(opcode == "10011"):
        sys.stdout.write(binary_converter(8,PC)+" ")
        Register_list[7] = 0 ################
        for i in Register_list:
            sys.stdout.write(binary_converter(16,i)+" ")
        sys.stdout.write("\n")
        address_list.append(visited_address)
        
        break
    
    for m in visited_address:
        if(m > maxi):
            maxi = m

    address_list.append(visited_address)
    cycle += 1
    

for i in reading:
    sys.stdout.write(i+"\n")


for i, j in zip(cycle_list, address_list):
    plt.scatter([i]*len(j),j)

plt.ylabel("Memory Address")
plt.xlabel("Cycles")
#plt.xticks(range(1,cycle+1))
#plt.yticks(range(0,max(maxi, PC) +1))
plt.show()