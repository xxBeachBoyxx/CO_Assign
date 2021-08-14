from sys import stdin

import sys

from pass1 import variable_list,label_list,instuction_count,x;

def binary_converter(a):
    ans = ""
    if(a == 0 or a == 1):
        return "0000000" + a
    while(a != 0 and a != 1):
        ans += f"{a%2}"
        a = a//2
    ans += f"{a}"
    ans = ans[::-1]
    n = len(ans)
    return "0"*(8-n) + ans

def solver(list1, start_index, operation_dict, register_dict):
    ans = ""
    if(operation_dict[list1[start_index]][1] == "A"):
        ans = operation_dict[list1[start_index]][0] + "00"
        for i in list1[start_index+1:]:
            ans += register_dict[i]
        return ans
    elif(operation_dict[list1[start_index]][1] == "B"):
        ans = operation_dict[list1[start_index]][0] + register_dict[list1[start_index+1]]
        a = binary_converter(register_dict[list1[start_index+2]])
        ans = ans+ a

    elif(operation_dict[list1[start_index]][1] == "C"):
        ans = operation_dict[list1[start_index]][0]+"00000"
        for i in list1[start_index+1:]:
            ans += register_dict[i]
        return ans

    elif(operation_dict[list1[start_index]][1] == "D"):
        ans = operation_dict[list1[start_index]][0]+register_dict[list1[start_index+1]]
        k=variable_list[list1[start_index+2]]+instuction_count
        g = binary_converter(k)
        return ans+g

    elif(operation_dict[list1[start_index]][1] == "E"):
        ans = operation_dict[list1[start_index]][0]+register_dict[list1[start_index+1]]
        h=variable_list[list1[start_index+2]]+instuction_count
        i = binary_converter(h)
        return ans+i

    elif(operation_dict[list1[start_index]][1] == "F"):
        ans = operation_dict[list1[start_index]][0]+"00000000000"
        return ans
        
    ## Checking for mov instruction
    elif(len(list1[start_index:])==3): ## label: mov d1 d2 // label1: mov r $4 //label1: mov r2 R2 $
        if(list1[start_index]=="mov" and list1[-1][0]=="$" and (int(list1[start_index+2][1:])>=0 and int(list1[start_index+2][1:])<=255)):
            if(list1[start_index+1] in register_dict.keys()):
                ans = "00010" + list1[start_index+1] + binary_converter(list1[-1][1:]) # B type 
        if(list1[start_index]=="mov"):
            if(list1[1] in register_dict.keys()):
                if(list1[2] in register_dict.keys()):
                    ans = "00011" + list1[start_index+1] + list1[start_index+2]
        return ans
    

def checkerror(list1):  
    if list1[0] in operation_dict.keys():
        if len(list1)==4: # len=4-->possible types:A
            if operation_dict[list1[0]][1]=="A": #checks if instruction is A 
                if list1[1] in register_dict.keys() and list1[2] in register_dict.keys() and list1[3] in register_dict.keys(): #syntax check
                    return True
        elif len(list1)==3: # len=3-->possible types:B,C,D
            if operation_dict[list1[0]][1]=="B": #checks if instruction is B
                if list1[1] in register_dict.keys() and list1[2][0]=="$" and (int(list1[2][1:])>=0 and int(list1[2][1:])<=255): #syntax check
                    return True
            elif operation_dict[list1[0]][1]=="C": #checks if instruction is C
                if list1[1] in register_dict.keys() and list1[2] in register_dict.keys(): #syntax check
                    return True
            elif operation_dict[list1[0]][1]=="D": #checks if instruction is D
                if list1[1] in register_dict.keys(): 
                    if list1[2] in variable_list.keys():   #syntax check
                        return True
            elif list1[0]=="mov":
                pass
        elif len(list1)==2: # len=2-->possible types:E
            if operation_dict[list1[0]][1]=="E": #checks if instruction is E
                if list1[1] in label_list.keys():          #syntax check
                    return True
        elif len(list1)==1: # len=1-->possible types:F
            if operation_dict[list1[0]][1]=="F" and i==x: #checks if instruction is F and if it is the last instruction
                return True
    return False


operation_dict = {    # Does not have the two mov instructions
"add":["00000","A"],  
"sub":["00001","A"],
"ld":["00100","D"],
"st":["00101","D"],
"mul":["00110","A"],
"div":["00111","C"],
"rs":["01000","B"],
"ls":["01001","B"],
"xor":["01010","A"],
"or":["01011","A"],
"and":["01100","A"],
"not":["01101","C"],
"cmp":["01110","C"],
"jmp":["01111","E"],
"jlt":["10000","E"],
"jgt":["10001","E"],
"je":["10010","E"],
"hlt":["10011","F"]}

register_dict = {
"R0":"000",
"R1":"001",
"R2":"010",
"R3":"011",
"R4":"100",
"R5":"101",
"R6":"110",
"R7":"111"
}
i=0
for line in stdin:
    list1 = (line.strip()).split()
    if(list1[0] == "var" or line == "\n"):
        continue
    if(list1[0][-1] == ":"):
        if(list1[0][:-1] in operation_dict.keys()):  # Checks if a operation name is used as a label
            raise RuntimeError(" Error in the assembly code ")
        else:
            if(checkerror(list1[1:])): #checks if there are no errors in the instruction that follows after label
                   sys.stdout.write(solver(list1,1,operation_dict,register_dict))
            else:
                raise RuntimeError(" Error in the assembly code ")
    else:
        if(checkerror(list1)): #checks if there are no errors
            sys.stdout.write(solver(list1,0,operation_dict,register_dict))
        else:
            raise RuntimeError(" Error in the assembly code ")
    i+=1