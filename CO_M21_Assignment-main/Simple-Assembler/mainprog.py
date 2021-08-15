import sys
from sys import stdin
reading = stdin.read()
reading = reading.split("\n")


error=False

def error_finderv(list1,er_ln): #
    if(len(list1) != 2): # Checks if the variable initialization instruction has more than two strings.
        print("Line:",er_ln+1,"General Syntax Error")
         
        return True
    else:
        for i in list1[1]:
            if((i.isalnum() or i == "_")): # Checks if the variable name has just alphanumeric characters or underscores.
                pass
            else:
                print("Line:",er_ln+1,"General Syntax Error")
                return True
    return False

def error_finderl(list1,er_ln):
    colon_count = 0
    for i in list1:
        if ":" in i:
            colon_count += 1 
    
    if(colon_count > 1): # Checks if there are more than one colon used in a label initialization instruction.
        print("Line:",er_ln+1,"General Syntax Error")
        return True

    for i in list1[0][:-1]:
        if((i.isalnum() or i == "_")): # Checks if the label name has just alphanumeric characters or underscores.
            pass
        else:
            print("Line:",er_ln+1,"General Syntax Error")
            return True
    return False
    
def error_finderf(variable_list, label_list, variable_name_list, label_name_list):
    vkey = variable_list.keys()
    lkey = label_list.keys()
    
    intersection = [value for value in vkey if value in lkey]
    if(intersection != []):  # Checks if a variable name is used as a label or vice a versa.
        print("Line: ",variable_list[intersection[0]]+1," Misuse of labels as variables or vice-versa")
        return True

    if(len(variable_name_list) != len(list(set(variable_name_list)))): # Checks if a variable initialization is done more than once.
        for j in list(set(variable_name_list)):
            if variable_name_list.count(j)>1:
                print("Line:",variable_list[j]+1, "Multiple Initialisation of the same variable")
                return True        
    
    if(len(label_name_list) != len(list(set(label_name_list)))):
        for j in list(set(label_name_list)):
            if label_name_list.count(j)>1:
                print("Line:",label_list[j]+1-variable_count," General Syntax Error")
                return True

    variable_values = variable_list.values()

    for i in range(len(variable_values)): # Checks if all the variable initialization instructions are contiguous or not.
        if i in variable_values:
            pass
        else:
            print("Line:",i+1,"Error: Variable not defined at appropriate time")
            return True
    return False

variable_list = {}
variable_name_list = []
label_list = {}
label_name_list = []
variable_count = 0

x = 0

for line in reading:
    list1 = (line.strip()).split()

    if(len(line)==0):
        continue
    if(list1[0] == "var"):
        pass
    elif(list1[0][-1] == ":"):
        pass
    x += 1

y=0
for line in reading:
    #print(line)
    list1 = (line.strip()).split()

    #print(list1)
    if(len(line)==0):
        continue
    if(list1[0] == "var"):
        error=error_finderv(list1,y)
        if error==True:
            break
        else:
            variable_list[list1[1]] = y  # Real memory location of the variable instruction is x + instruction_count
            variable_name_list.append(list1[1])
            variable_count += 1
    elif(list1[0][-1] == ":"):
        error=error_finderl(list1,y)
        if error==True:
            break
        label_list[list1[0][:-1]] = y - variable_count
        label_name_list.append(list1[0][:-1])
    y+=1

error=error or error_finderf(variable_list,label_list,variable_name_list, label_name_list)

instuction_count = y - variable_count
#print(variable_list)
######################################################################################3
# pass 2
def binary_converter(a): 
    a = int(a)
    ans = ""
    if(a == 0 or a == 1):
        return "0000000" + str(a)
    while(a != 0 and a != 1):
        ans += str(a%2)
        a = a//2
    ans += str(a)
    ans = ans[::-1]
    n = len(ans)
    return "0"*(8-n) + ans

def solver(list1, start_index, operation_dict, register_dict):
    ans = ""

     ## label: mov d1 d2 // label1: mov r $4 //label1: mov r2 R2 $
    
    if(list1[start_index]=="mov" and list1[-1][0]=="$" and (int(list1[start_index+2][1:])>=0 and int(list1[start_index+2][1:])<=255)):
        if(list1[start_index+1] in register_dict.keys()):
            ans = "00010" + register_dict[list1[start_index+1]] + binary_converter(list1[-1][1:]) # B type 
            return ans
    if(list1[start_index]=="mov"):    #mov type C
        if(list1[start_index+1] in register_dict.keys()):
            if(list1[start_index+2] in register_dict.keys()):
                ans = "00011" +"00000"+ register_dict[list1[start_index+1]] + register_dict[list1[start_index+2]]
            elif(list1[start_index+2]=="FLAGS"):
                ans = "00011" +"00000"+ register_dict[list1[start_index+1]]+"111"
            return ans
    
    if(operation_dict[list1[start_index]][1] == "A"):
        ans = operation_dict[list1[start_index]][0] + "00"
        for i in list1[start_index+1:]:
            ans += register_dict[i]
        return ans
    elif(operation_dict[list1[start_index]][1] == "B"):
        ans = operation_dict[list1[start_index]][0] + register_dict[list1[start_index+1]]
        a = binary_converter(list1[start_index+2][1:])
        #a = binary_converter(register_dict[list1[start_index+2]])
        ans = ans+ a
        return ans

    elif(operation_dict[list1[start_index]][1] == "C"):
        ans = operation_dict[list1[start_index]][0]+"00000"
        for i in list1[start_index+1:]:
            ans += register_dict[i]
        return ans

    elif(operation_dict[list1[start_index]][1] == "D"):
        ans = operation_dict[list1[start_index]][0]+register_dict[list1[start_index+1]]
        k=int(variable_list[list1[start_index+2]])+instuction_count
        g = binary_converter(k)
        return ans+g

    elif(operation_dict[list1[start_index]][1] == "E"):
        ans = operation_dict[list1[start_index]][0]+"000"
        h=label_list[list1[start_index+1]]
        i = binary_converter(h)
        return ans+i

    elif(operation_dict[list1[start_index]][1] == "F"):
        ans = operation_dict[list1[start_index]][0]+"00000000000"
        return ans
        
    ## Checking for mov instruction
    

def checkerror(list1,i): 
    #print(x," ",i) 

    if list1[0]=="mov" or list1[0] in operation_dict.keys():
        if len(list1)==4 and i!=x-1: # len=4-->possible types:A
            if operation_dict[list1[0]][1]=="A": #checks if instruction is A 
                if list1[1] in register_dict.keys() and list1[2] in register_dict.keys() and list1[3] in register_dict.keys(): #syntax check
                    return True
        elif len(list1)==3 and i!=x-1: # len=3-->possible types:B,C,D
            if list1[0]=="mov":
                if list1[1] in register_dict.keys() and list1[2][0]=="$" and (int(list1[2][1:])>=0 and int(list1[2][1:])<=255):
                    return True
                elif list1[1] in register_dict.keys() and (list1[2] in register_dict.keys() or list1[2]=="FLAGS"):
                    return True
            elif operation_dict[list1[0]][1]=="B": #checks if instruction is B
                if list1[1] in register_dict.keys() and list1[2][0]=="$" and (int(list1[2][1:])>=0 and int(list1[2][1:])<=255): #syntax check
                    return True
            elif operation_dict[list1[0]][1]=="C": #checks if instruction is C
                if list1[1] in register_dict.keys() and list1[2] in register_dict.keys(): #syntax check
                    return True
            elif operation_dict[list1[0]][1]=="D": #checks if instruction is D
                if list1[1] in register_dict.keys(): 
                    if list1[2] in variable_list.keys():   # {"x":0}
                        return True
            
        elif len(list1)==2 and i!=x-1: # len=2-->possible types:E
            if operation_dict[list1[0]][1]=="E": #checks if instruction is E
                if list1[1] in label_list.keys():          #syntax check
                    return True
        elif len(list1)==1: # len=1-->possible types:F
            if operation_dict[list1[0]][1]=="F" and i==x-1: #checks if instruction is F and if it is the last instruction
                #print(x," ",i)
                return True
    
    return False

def generate_error(list1,error_line):
    if list1[0]=="mov" or list1[0] in operation_dict.keys():
        if error_line==x-1:
            if operation_dict[list1[0]][1]!="F":
                print("Line : ",error_line+1,"Missing hlt instruction")
                return
        if (list1[0]=="mov"):
            if(len(list1)==3 and list1[2][0]=="$"):
                if len(list1)!=3 :
                    print("Line : ",error_line+1,"Wrong syntax used for instructions")
                    return
                if list1[1] not in register_dict.keys():
                    print("Line : ",error_line+1,"Typos in instruction name or register name")
                    return
                if list1[2][0]!="$":
                    print("Line : ",error_line+1,"General syntax error")
                    return
                if (int(list1[2][1:])>=0 and int(list1[2][1:])<=255):
                    pass
                else:
                    print("Line : ",error_line+1,"Illegal Immediate values")
                    return
            elif len(list1)==3 and (list1[2] in register_dict.keys() or list1[2]=="FLAGS"):
                if list1[1] in register_dict.keys() :
                    pass
                else:
                    print("Line : ",error_line+1,"Typos in instruction name or register name")
                    return  
            else:
                print("Line : ",error_line+1,"General Syntax Error")  

        if operation_dict[list1[0]][1] =="A" and line_no!=x-1:
            if len(list1)!=4:
                print("Line : ",error_line+1,"Wrong syntax used for instructions")
                return
            if list1[1] in register_dict.keys() and list1[2] in register_dict.keys() and list1[3] in register_dict.keys():
                pass
            else:
                print("Line : ",error_line+1,"Typos in instruction name or register name")
                return
        elif operation_dict[list1[0]][1]=="B" and line_no!=x-1:
            if len(list1)!=3:
                print("Line : ",error_line+1,"Wrong syntax used for instructions")
                return
            if list1[1] not in register_dict.keys():
                print("Line : ",error_line+1,"Typos in instruction name or register name")
                return
            if list1[2][0]!="$":
                print("Line : ",error_line+1,"General syntax error")
                return
            if (int(list1[2][1:])>=0 and int(list1[2][1:])<=255):
                pass
            else:
                print("Line : ",error_line+1,"Illegal Immediate values")
                return
        elif operation_dict[list1[0]][1]=="C" and line_no!=x-1:
            if len(list1)!=3:
                print("Line : ",error_line+1,"Wrong syntax used for instructions")
                return
            if list1[1] in register_dict.keys() and list1[2] in register_dict.keys():
                pass
            else:
                print("Line : ",error_line+1,"Typos in instruction name or register name")
                return
        elif operation_dict[list1[0]][1]=="D" and line_no!=x-1:
            if len(list1)!=3:
                print("Line : ",error_line+1,"Wrong syntax used for instructions")
                return
            if list1[1] in register_dict.keys(): 
                    if list1[2] in variable_list.keys():   
                        pass
                    else:
                        print("Line : ",error_line+1,"Use of undefined variables")
                        return
            else:
                print("Line : ",error_line+1,"Typos in instruction name or register name")
                return
        elif operation_dict[list1[0]][1]=="E" and line_no!=x-1:
            if len(list1)!=2:
                print("Line : ",error_line+1,"Wrong syntax used for instructions")
                return
            if list1[1] in label_list.keys():
                pass
            else:
                print("Line : ",error_line+1,"Use of undefined labels")
        elif operation_dict[list1[0]][1]=="F" and line_no==x-1:
            if len(list1)!=0:
                print("Line : ",error_line+1,"Wrong syntax used for instructions")
        else:
            print("Line : ",error_line+1,"hlt not being used as the last instruction")
    else:
        print("Line : ",error_line+1,"Typos in instruction name or register name")



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
"R6":"110"
}

if error==False:
    line_no=0
    for line in reading:
        list1=(line.strip()).split()
        if(len(line)==0):
            continue
        if(list1[0] == "var"):
            if(line_no!=x-1):
                line_no = line_no+1
                continue
        if(list1[0][-1]==":"):
            if(list1[0][:-1] in operation_dict.keys()):  # Checks if a operation name is used as a label
                print("Line :",line_no+1,"General Syntax Error")
                error=True
                break
            else:
                if(len(list1[1:])==0):
                    print("Line :",line_no+1,'General Syntax Error')
                    error=True
                    break
                elif(checkerror(list1[1:],line_no)): #checks if there are no errors in the instruction that follows after label
                    pass
                else:
                    generate_error(list1[1:],line_no)
                    error=True
                    break
        else:
            if(checkerror(list1,line_no)): #checks if there are no errors
                #print("check")
                pass
            else:
                generate_error(list1[0:],line_no)
                error=True
                break
        line_no+=1



if(error==False):
    ln=0
    #print(x)
    for line in reading:
        #print(line)
        list1 = (line.strip()).split()
        #print(list1)
        if(len(line)==0):
            continue
        if(list1[0] == "var"):
            if(ln!=x-1):
                ln = ln+1
                continue
        if(list1[0][-1] == ":"):
            if(list1[0][:-1] in operation_dict.keys()):  # Checks if a operation name is used as a label
                print("Line : ",ln+1,"General Syntax error")
            else:
                if(checkerror(list1[1:],ln)): #checks if there are no errors in the instruction that follows after label
                    print(solver(list1,1,operation_dict,register_dict))
                else:
                    print("Line : ",ln+1,"General Syntax Error")
        else:
            if(checkerror(list1,ln)): #checks if there are no errors
                #print("check")
                print(solver(list1,0,operation_dict,register_dict))
            else:
                print("Line : ",ln+1,"General Syntax error")
        ln+=1

