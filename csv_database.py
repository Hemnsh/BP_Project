import csv, shlex

def is_int(s):
    ##called on handle_type_value
    try:
        int(s)
        return True
    except:
        return False
              
def is_float(s):
    ##called on handle_type_value
    try:
        float(s)
        return True
    except:
        return False


def handle_type_value(lst , types):
    ##called on main
    ##handling type of insert value

    i = 0
    for element in lst:
        if types[i][1] == 'int' and is_int(element)== False : 
            print('type input error: Please enter the correct type', types[i])
        elif types[i][1] == 'float' and is_float(element) == False:
            print('type input error: Please enter the correct type', types[i])
        else:
            pass
        i += 1
    return True



def handle_error_write(user_input):
    ##called on main , several times
    ##hand writing or typing error
    ## create
    if len(user_input) >= 2 and user_input[0] == 'create' and user_input[1] == "table":
        return True
    ## insert
    if len(user_input) >= 4 and user_input[0] == 'insert' and user_input[1] == "into" and user_input[3] == "values":
        return True
    ## select
    Select = False
    From = False
    Where = False
    for i in user_input:
        if i == "select":
            Select = True
        if i == "from":
            From = True
        if i == "where":
            Where = True
    if Select and From and Where:
        return True
    print('Syntax error: Please enter the correct syntax.')
    return False
    

def handle_create(schema,table_name):
    ##called on main
    ##create csv
    with open(table_name , 'w' , newline='') as file:
        writer = csv.writer(file)
        writer.writerow(schema)



def handle_insert(values,table_name):
    ##called on main
    ##insert csv
    with open(table_name , 'a' , newline='') as file:
        writer = csv.writer(file)
        writer.writerow(values)


def handle_select(table_name , type):
    ##called on main
    ##select from csv
    with open(table_name , 'r' ) as file:
        csv_file = csv.DictReader(file)
        data = []
        for i in list(csv_file):
            data.append(i)
    return data



def handle_select_condition(type_dic,condition, data ):
    ##called on main
    ##handling on select condition for print

    
    if(len(condition)==1):
        condition = condition[0].split("=")
        if(len(condition)==1):
            condition = condition[0].split("<")
            if(len(condition)==1):
                condition=condition[0].split(">")
                condition.insert(1,">")
            else:
                condition.insert(1,"<")
        else:
            condition.insert(1,"=")


    for x in range(len(condition)):
        if condition[x] =='>' or condition[x] == '<' or condition[x] == '=':
            column_name, tag, value = condition[x-1], condition[x], condition[x+1]
    result = []
    try:
        value = int (value) if type_dic[column_name] == "int" else value
    except:
        pass
    for i in range(len(data)):
        for k in data[i].keys():
            if (type_dic[k]=="int"):
                try:
                    data[i][k] = int(data[i][k])     
                except:
                    print("Invalid data type.")
        
    if(type_dic[column_name]=="int"):
        if(type(value) != int):
            print (f"type error: The column name {column_name} does not match the type {type(value)}")
            return
    elif (type_dic[column_name]=="string"):
        if(type(value) != str):
            print (f"type error: The column name {column_name} does not match the type {type(value)}")
            return
    for data in data:
        if(type(data[column_name])==str):
            if (data[column_name].lower()) == value:
                result.append(data)
        elif tag == ">":
            if (data[column_name]) > value:
                result.append(data)
        elif tag == "=":
            if (data[column_name]) == value:
                result.append(data)
        else:
            if (data[column_name]) < value:
                result.append(data)

    return result



def handle_select_cloumn_name(column_names, data):
    ##called on main
    ##handling on select condition for print
    if column_names == ["*"]:
        return data
    result = []

    for i in range(len(data)):
        temp = {}
        for column in column_names:
            if column in data[i].keys():
                temp[column] = data[i][column]
            else:
                return (f"column name error: The column name {column} does not exist.")
        result.append(temp)
    return result




def split(string):
    #split on user_input
    string = [i.replace('(', '').replace(')', '').replace(',', ' ') for i in string]
    string = shlex.split(''.join(string))
    return string

def saveTypesWhenCreate(user_input):
 
    # check if the table name is already exist
    try:
        with open('schema.txt', 'r') as file:
            for line in file:
                if line.split()[0] == user_input[2]:
                    print('table name error: The table name is already exist.')
                    return False
    except:
        pass 
    #save types when create into a schema.txt file
    with open('schema.txt', 'a') as file:
        file.write(user_input[2] + "\n")
        for i in range(3,len(user_input) , 2):
            file.write(user_input[i] + ' ' +user_input[i+1])
            file.write('\n')

def readTypesWhenSelect(table_names,table_title):
    #read types when select from a file
    l = []
    flag = False
    with open('schema.txt', 'r') as file:
        for line in file:
            line = line.split()
            if(len(line)==1 and line[0] == table_title):
                flag = True
                continue
            elif(len(line)==1):
                if(flag):
                    break
                else:
                    continue
            if(flag):
                for table_name in table_names:
                    if line[0] == table_name:
                        l.append(line[1])
    return l

def readTypesFromTableName(table_title,withName=False):
    #read types when insert into a file
    l = []
    dic = {}
    flag = False
    with open('schema.txt', 'r') as file:
        for line in file:
            line = line.split()
            if(len(line)==1 and line[0] == table_title):
                flag = True
                continue
            elif(len(line)==1):
                if(flag):
                    break
                else:
                    continue
            if(flag):
                if(withName):
                    dic[line[0]]=line[1]
                else:
                    l.append(line)
    return dic if withName else l


def create (user_input):
    file_name = str(user_input[2]+'.csv')
    handle_create(schema = user_input[3::2],table_name = file_name)  
    saveTypesWhenCreate(user_input)
    types = [ user_input[i+1]  for i in range (3,len(user_input) , 2)]
    type_d = {user_input[i]:user_input[i+1]  for i in range (3,len(user_input) , 2)}

def insert(user_input):
    file_name = str(user_input[2]+'.csv')
    columnsIndex = user_input.index('values')
    columns = user_input[columnsIndex+1:]
    tableName = user_input[columnsIndex-1]
    types = readTypesFromTableName(tableName)
    if(len(columns)!=len(types)):
        print(f"Invalid number of inputs:input parameters should be {len(types)} not {len(columns)}")
        return
    type_d = {n:t[0] for n,t in zip(columns , types)} 
    while True:
        if handle_type_value(user_input[4:] , types):
            handle_insert(values = user_input[4:] , table_name = file_name )
            break  
        else:
            while True:
                user_input = input().lower()
                user_input = split(user_input)
                if handle_error_write(user_input=user_input) == True:
                    break

def select(user_input):
    columnsIndex = user_input.index('from')
    columns = user_input[1:columnsIndex]
    types = readTypesWhenSelect(columns,user_input[columnsIndex+1])
    allTypes = readTypesFromTableName(user_input[columnsIndex+1],True)

    file_name = str(user_input[2+len(columns)]+'.csv')
    data = handle_select(file_name  , types)
    data = handle_select_condition(allTypes,condition=user_input[4+len(columns):], data=data  )
    if(data == None):
        return
    elif(data==[]):
        print("No data found")
        return
    data = handle_select_cloumn_name(columns, data)
    print(data)

def handle_input(user_input):
    if user_input[0] == 'create':
        create(user_input)
    elif user_input[0] == 'insert':
        insert(user_input)
    elif user_input[0] == 'select':
        select(user_input)

def main():
    pass


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    n = int(input())
    while 0<n:

        types = []
        while True:
            user_input = input().lower()
            user_input = split(user_input)
            if handle_error_write(user_input=user_input) == True:
                break

        n-=1
        handle_input(user_input)
                 

