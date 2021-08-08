from sys import stdin

def error_finderv(list1):
    if(len(list1) != 2):
        raise RuntimeError(" Error in the assembly code ")
    for i in list1[1]:
        if((i.isalnum() or i == "_")):
            pass;
        else:
            raise RuntimeError(" Error in the assembly code ")

def error_finderl(list1):
    colon_count = 0
    for i in list1:
        if ":" in i:
            colon_count += 1
    
    if(colon_count != 1):
        raise RuntimeError(" Error in the assembly code ")

    for i in list1[0][:-1]:
        if((i.isalnum() or i == "_")):
            pass
        else:
            raise RuntimeError(" Error in the assembly code ")

    
def error_finderf(variable_list, label_list):
    vkey = variable_list.keys()
    lkey = label_list.keys()
    
    intersection = [value for value in vkey if value in lkey]
    if(intersection != []):
        raise RuntimeError(" Error in the assembly code ")

    if(len(vkey) != len(list(set(vkey)))):
        raise RuntimeError(" Error in the assembly code ")
    
    variable_values = variable_list.values()

    for i in range(len(variable_values)):
        if i in variable_values:
            pass
        else:
            raise RuntimeError(" Error in the assembly code ")

    

variable_list = {}
label_list = {}
variable_count = 0
x = 0
for line in stdin:
    list1 = (line.strip()).split();
    if(list1[0] == "var"):
        error_finderv(list1)
        variable_list[list1[1]] = x;
        variable_count += 1
    elif(list1[0][-1] == ":"):
        error_finderl(list1)
        label_list[list1[0][:-1]] = x - variable_count
    x += 1

error_finderf(variable_list,label_list)

print("ok")