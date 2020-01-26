import os

def ConvertFile(Old, New, Type):

    Set = 0
    Parameters = []

    for Line in Old:
        Line = Line.strip()
        Line = Line.split()

        if(Line[0] == "CREATE" and Line[1] == "TABLE"):
        # This is to start creating the table in the JSON file

            if(Type == ".json"):
            # JSON File
                New.write("{\n")
                New.write('  "' + Line[2] + '":\n')
                New.write("  [\n")
            else:
            # JavaScript File
                New.write("var " + Line[2] + " = [\n")

            Set = 1
            continue

        if(Set == 1):
        # This is to get the parameters of the table
            if(len(Line) > 2 and Line[2] == ");"):
                Parameters.append(Line[0])
                Set = 2
            elif(Line[0] == ");"):
                Set = 2
            else:
                Parameters.append(Line[0])

        if(Line[0] == "INSERT"):
            if(Set == 3):
                New.write(",\n")
            
            ValueList = Line[3]
            
            for i in range(len(Line)):
                if(i <= 3):
                    continue
                ValueList = ValueList + " " + Line[i]
                
            ValueList = ValueList[7:]
            ValueList = ValueList[:-2]
            ValueList = ValueList.split(",")

            New.write("    {\n")
            Set = 3

            for i in range(len(Parameters)):
                New.write('      "' + Parameters[i] + '": ' + ValueList[i])
                if(i == (len(Parameters) - 1)):
                    New.write("\n")
                else:
                    New.write(",\n")
                    
            New.write("    }")
            
    New.write("\n")

    if(Type == ".json"):
        New.write("  ]\n")
        New.write("}\n")
    else:
        New.write("  ];")

# ----------------------------------------------------------------
# The point of this program is to convert a SQL table to a JSON File

Done = False

while(not Done):
    Exist = False

    while(not Exist):
        Name = input("Enter name of SQL table file: \n")
        
        try:
            SQL = open(os.getcwd() + "/" + Name + ".sql", "r")
        except:
            print("File not found! \n")
        else:
            Exist = True

    FOO = False

    while(not FOO):
        Type = input("JSON or JavaScript? ")
        Type = Type.lower()

        if(Type == "json"):
            Type = ".json"
            FOO = True
        elif(Type == "javascript"):
            Type = ".js"
            FOO = True
        else:
            print("What? I didn't understand that. Which file type? ")

    JSON = open(os.getcwd() + "/" + Name + Type, "w")

    ConvertFile(SQL, JSON, Type)

    JSON.close()

    Quit = input("Do you want to quit? Press 1 to quit.")
    if(Quit == "1"):
        Done = True

print("Goodbye!")
