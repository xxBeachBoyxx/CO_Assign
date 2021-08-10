from sys import stdin

def error_finderv(list1):
    if(len(list1) != 2): # Checks if the variable initialization instruction has more than two strings.
        raise RuntimeError(" Error in the assembly code ") 
    for i in list1[1]:
        if((i.isalnum() or i == "_")): # Checks if the variable name has just alphanumeric characters or underscores.
            pass;
        else:
            raise RuntimeError(" Error in the assembly code ")

def error_finderl(list1):
    colon_count = 0
    for i in list1:
        if ":" in i:
            colon_count += 1
    
    if(colon_count != 1): # Checks if there are more than one colon used in a label initialization instruction.
        raise RuntimeError(" Error in the assembly code ")

    for i in list1[0][:-1]:
        if((i.isalnum() or i == "_")): # Checks if the label name has just alphanumeric characters or underscores.
            pass
        else:
            raise RuntimeError(" Error in the assembly code ")

    
def error_finderf(variable_list, label_list, variable_name_list, label_name_list):
    vkey = variable_list.keys()
    lkey = label_list.keys()
    
    intersection = [value for value in vkey if value in lkey]
    if(intersection != []):  # Checks if a variable name is used as a label or vice a versa.
        raise RuntimeError(" Error in the assembly code ")

    if(len(variable_name_list) != len(list(set(variable_name_list)))): # Checks if a variable initialization is done more than once.
        raise RuntimeError(" Error in the assembly code ")
    
    if(len(label_name_list) != len(list(set(label_name_list)))):
        raise RuntimeError(" Error in the assembly code ")

    variable_values = variable_list.values()

    for i in range(len(variable_values)): # Checks if all the variable initialization instructions are contiguous or not.
        if i in variable_values:
            pass
        else:
            raise RuntimeError(" Error in the assembly code ")

    

variable_list = {}
variable_name_list = []
label_list = {}
label_name_list = []
variable_count = 0
x = 0
for line in stdin:
    list1 = (line.strip()).split();
    if(list1[0] == "var"):
        error_finderv(list1)
        variable_list[list1[1]] = x;
        variable_name_list.append(list1[1])
        variable_count += 1
    elif(list1[0][-1] == ":"):
        error_finderl(list1)
        label_list[list1[0][:-1]] = x - variable_count
        label_name_list.append(list1[0][:-1])
    x += 1

error_finderf(variable_list,label_list,variable_name_list, label_name_list)

print("ok")