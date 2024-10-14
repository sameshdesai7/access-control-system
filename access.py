import sys
import os.path

def print2Darray(arr):
    for i in range(len(arr)):
        print(arr[i])

usedFirstUserAdd = False
isLoggedIn = False
currentUser = ""
isRoot = False

#create 2d array to store groups and members during execution
groupsAndMembers = []
files = []

#clear groups.txt at start
groups = open("groups.txt", "w")

#clear accounts.txt at start
accounts = open("accounts.txt", "w")

#clear audit.txt at a start
audit = open("audit.txt", "w")

#create files.txt
fileInit = open("files.txt", "w")

#clear all content in filenames stored in files.txt at start
for line in open("files.txt"):
    lineArr = line.split(" ")
    temp = open(lineArr[0], "w")

#delete files stored in first param of each line in files.txt at start
for line in open("files.txt"):
    lineArr = line.split(" ")
    #remove file at lineArr[0]
    if os.path.exists(lineArr[0]):
        os.remove(lineArr[0])


#Show Program Started
print("Entered Program")

#Accept File Input
file_name = sys.argv[1]
fp = open(file_name)
contents = fp.readlines()

#open audit file to append command history to
audit = open("audit.txt", "a")

for line in contents:
    line.rstrip('\n')

    lineArr = line.split(" ")
    
    #add user
    if lineArr[0] == "useradd":
        

        isAllowed = 1

        accounts = open("accounts.txt", "r")

        #check for duplicate usernames
        for account in accounts:
            accountArr = account.split(" ")
            if accountArr[0].strip("\n") == lineArr[1].strip("\n"):
                print("Account " + lineArr[1] + " already exists")
                #write console output to audit.txt
                audit.write("Account " + lineArr[1] + " already exists\n")

                isAllowed = 0
        
        if(isAllowed == 0):
            continue
        
        if(isAllowed == 1):

            #check if user is root or is first run
            if ((not usedFirstUserAdd) or isRoot):
                usedFirstUserAdd = True
                accounts = open("accounts.txt", "a")
                lineArr[2] = lineArr[2].strip("\n")

                #check to make sure username doesnt contain / or :
                if "/" in lineArr[1] or ":" in lineArr[1]:
                    print("Username contains invalid character")
                    continue
                
                #check to make sure password does not contain carriage return, form feed, horizontal tab, newline, vertical tab, or space
                if any(char in lineArr[2] for char in ('\r', '\n', '\t', '\v', '\b')):
                    print("Password contains invalid character")
                    continue
                else:
                    print("Adding User: " + lineArr[1])
                    accounts.write(lineArr[1])
                    accounts.write(" ")
                    accounts.write(lineArr[2])
                    accounts.write("\n")        
                    audit.write("Adding User: " + lineArr[1] + "\n")
            else:
                print("Error: Only the root use can create accounts")
                #write console output to audit.txt
                audit.write("Error: Only the root user can create accounts\n")
            continue

    #login
    elif lineArr[0] == "login":
        if(isLoggedIn):
            print("Please Logout before logging in with another account")
            #write console output to audit.txt
            audit.write("Please Logout before logging in with another account\n")
            continue
        else:
            accounts = open("accounts.txt", "r")
            accounts = accounts.readlines()
            
            for account in accounts:
                accountArr = account.split(" ")
                #if the passing in credentials are equal to a line in the accounts.txt file
                if(accountArr[0].strip("\n") == lineArr [1].strip("\n")) & (accountArr[1].strip("\n") == lineArr[2].strip("\n")):
                    isLoggedIn = True
                    currentUser = accountArr[0]
                    print("Logging in user: " + currentUser)
                    #write console output to audit.txt
                    audit.write("Logging in user: " + currentUser + "\n")
                    if accountArr[0] == "root":
                        isRoot = True
                else:
                    continue
            if not isLoggedIn:
                print("Login failed: invalid username or password")
                #write console output to audit.txt
                audit.write("Login failed: invalid username or password\n")
        continue

    #end
    elif lineArr[0] == "end":
        #before logout export groupsandmembers to groups.txt
        groupsFile = open("groups.txt", "w")
        for group in groupsAndMembers:
            group = str(group)
            group = group.replace("[", "")
            group = group.replace("]", "")
            group = group.replace("'", "")
            group = group.replace(", ", " ")
            group = group.replace("\\n", "")
            groupsFile.write(group + "\n")
        #before logout export files to files.txt
        filesFile = open("files.txt", "w")
        for file in files:
            file = str(file)
            file = file.replace("[", "")
            file = file.replace("]", "")
            file = file.replace("'", "")
            file = file.replace(", ", " ")
            file = file.replace("\\n", "")
            filesFile.write(file + "\n")
        print("end")
        #write console output to audit.txt
        audit.write("end")
        continue

    #only allow the below functions to run if user is logged in
    if isLoggedIn == False:
        print("User must be logged in to execute " + lineArr[0] + " command")
        #write console output to audit.txt
        audit.write("User must be logged in to execute " + lineArr[0] + " command\n")
        continue
        
    #logout
    if lineArr[0].strip("\n") == "logout":
            
        isLoggedIn = False
        isRoot = False
        print("Logging out user: " + currentUser)
        #write console output to audit.txt
        audit.write("Logging out user: " + currentUser + "\n")
        continue
        

    #group add
    #add groups to the 2d array
    elif lineArr[0] == "groupadd":
        if isRoot:
            #check if group already exists
            if lineArr[1].strip("\n") in [item[0] for item in groupsAndMembers]:
                print("Error: Group " + lineArr[1].strip("\n") + " already exists")
                #write console output to audit.txt
                audit.write("Error: Group " + lineArr[1].strip("\n") + " already exists" + "\n")
                continue

            groupsAndMembers.append([lineArr[1].strip("\n")])
            print("Group added: " + lineArr[1].strip("\n"))
            #write console output to audit.txt
            audit.write("Group added: " + lineArr[1].strip("\n") + "\n")
        else: 
            print("Error: Only root can add groups")
            #write console output to audit.txt
            audit.write("Error: Only root can add groups" + "\n")

    #usergrp
    #adds user to a group
    elif lineArr[0] == "usergrp":
        if isRoot:
            for group in groupsAndMembers:
                if group[0] == lineArr[2].strip("\n"):
                    group.append(lineArr[1])
                    print("Added user: " + lineArr[1] + " to group " + lineArr[2].strip("\n"))
                    audit.write("Added user: " + lineArr[1] + " to group " + lineArr[2].strip("\n") + "\n")
        else:
            print("only root can add users to groups")
            audit.write("only root can add users to groups\n")
            
    #make file
    elif lineArr[0] == "mkfile":
        isAllowedCreate = 0

        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1].strip("\n") == "accounts.txt" or lineArr[1].strip("\n") == "groups.txt" or lineArr[1].strip("\n") == "files.txt" or lineArr[1].strip("\n") == "audit.txt":
            print("System file names cannot be used.")
            continue
        
        else:
            file_name_to_search = lineArr[1].strip("\n")
            for index, item in enumerate(files):
                if item[0] == file_name_to_search:
                    print("Error: File " + lineArr[1].strip("\n") + "already exists")
                    #write console output to audit.txt 
                    audit.write("Error: File " + lineArr[1].strip("\n") + "already exists" + "\n")
                    isAllowedCreate = 1
                    break

            if isAllowedCreate == 0:
                f = open(lineArr[1].strip("\n").strip(" "), "w")
                files.append([lineArr[1].strip("\n"), currentUser, "", "rw-", "---", "---"])
                print("Created file: " + lineArr[1].strip("\n") + " with owner " + currentUser + " and defult permissions") 
                #write console output to audit.txt
                audit.write("Created file: " + lineArr[1].strip("\n") + " with owner " + currentUser + " and defult permissions" + "\n")

    #chmod
    elif lineArr[0] == "chmod":

        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("System file names cannot be used.")
            continue

        #check if file exists
        if lineArr[1].strip("\n") not in [item[0] for item in files]:
            print("File" + lineArr[1] + " does not exist")
            audit.write("File" + lineArr[1] + " does not exist" + "\n")
            continue
        
        file_name_to_search = lineArr[1].strip("\n")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break
        
        if currentUser == "root" or currentUser == files[index][1]:
            files[index][3] = lineArr[2]
            files[index][4] = lineArr[3]
            files[index][5] = lineArr[4].strip("\n")
        
        else:
            print("Chmod Permission denied")
            audit.write("Chmod Permission denied" + "\n")
        
        print("Permissions for " + lineArr[1] + " changed to " + lineArr[2] + " " + lineArr[3] + " " + lineArr[4].strip("\n") + " by " + currentUser)
        audit.write("Permissions for " + lineArr[1] + " changed to " + lineArr[2] + " " + lineArr[3] + " " + lineArr[4].strip("\n") + " by " + currentUser + "\n")

    #chown
    elif lineArr[0] == "chown":

        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("File names cannot be used")
            continue

        #check if file exists
        if lineArr[1].strip("\n") not in [item[0] for item in files]:
            print("Chown Error: File" + lineArr[1] + " does not exist")
            #log to audit file
            audit.write("Chown Error: File" + lineArr[1] + " does not exist" + "\n")
            continue

        file_name_to_search = lineArr[1].strip("\n")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break
        
        if currentUser == "root":
            files[index][1] = lineArr[2].strip("\n")
        
        else:
            print("Chown Permission denied")
            audit.writeprint("Chown Permission denied\n")
        
        print("Owner of " + lineArr[1] + " changed to " + lineArr[2].strip("\n") + " by " + currentUser)
        audit.write("Owner of " + lineArr[1] + " changed to " + lineArr[2].strip("\n") + " by " + currentUser + "\n")
        

    #chgrp
    elif lineArr[0] == "chgrp":


        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("File names cannot be used")
            continue

        #check if file exists
        if lineArr[1].strip("\n") not in [item[0] for item in files]:
            print("File" + lineArr[1] + " does not exist")
            #log to audit
            audit.write("File" + lineArr[1] + " does not exit\n")
            continue

        file_name_to_search = lineArr[1].strip("\n")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break
        
        #if current user is root
        if currentUser == "root":
            files[index][2] = lineArr[2].strip("\n")
            print("Group for " + lineArr[1].strip("\n") + " changed to " + lineArr[2].strip("\n") + " by " + currentUser)
            #log to audit
            audit.write("Group for " + lineArr[1].strip("\n") + " changed to " + lineArr[2].strip("\n") + " by " + currentUser + "\n")
        
        #else if current user is a part of group being assigned
        elif currentUser != "root":
            for group in groupsAndMembers:
                if group[0] == lineArr[2].strip("\n"):
                    if len(group) > 1 and currentUser in group[1]:
                        files[index][2] = lineArr[2].strip("\n")
                        print("Group for " + lineArr[1].strip("\n") + " changed to " + lineArr[2].strip("\n") + " by " + currentUser)
                        audit.write("Group for " + lineArr[1].strip("\n") + " changed to " + lineArr[2].strip("\n") + " by " + currentUser + "\n")
                        break
                    else:
                        print("User " + currentUser + " not in group " + lineArr[2].strip("\n"))
                        audit.write("User " + currentUser + " not in group " + lineArr[2].strip("\n") + "\n")

        

    #read
    elif lineArr[0] == "read":

        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("File names cannot be used")
            continue

        #check if file exists
        if lineArr[1].strip("\n") not in [item[0] for item in files]:
            print("Read Error: File does not exist")
            audit.write("Read Error: File does not exist\n")
            continue

        file_name_to_search = lineArr[1].strip("\n")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break

        #owner permissions____group permissions______other permissions
        owner = files[index][1]
        fileGroup = files[index][2]
        ownerPermissions = files[index][3]
        groupPermissions = files[index][4]
        otherPermissions = files[index][5]

        inFileGroup = False
        #check if current user is in group specified in file
        for group in groupsAndMembers:
            if str(group[0]) == fileGroup:
                if currentUser in group[1]:
                    inFileGroup = True
                    break
        
        if(currentUser == owner and "r" in ownerPermissions):
            print("User " + currentUser + " reads " + lineArr[1].strip("\n") + " as: ") 
            audit.write("User " + currentUser + " reads " + lineArr[1].strip("\n") + " as: \n") 
        elif(currentUser in group and "r" in groupPermissions):
            print("User " + currentUser + " reads " + lineArr[1].strip("\n") + " as: ") 
            audit.write("User " + currentUser + " reads " + lineArr[1].strip("\n") + " as: \n") 
        elif("r" in otherPermissions):
            print("User " + currentUser + " reads " + lineArr[1].strip("\n") + " as: ") 
            audit.write("User " + currentUser + " reads " + lineArr[1].strip("\n") + " as: \n") 
        else:
            print("User " + currentUser + " denied read permission for " + lineArr[1].strip("\n"))
            audit.write("User " + currentUser + " denied read permission for " + lineArr[1].strip("\n") + "\n")
            continue

        #read file contents
        with open(file_name_to_search) as f:
            lines = f.readlines()
            for line in lines:
                print(line.strip("\n"))
                audit.write(line)
                

    #write
    elif lineArr[0] == "write":
        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("File names cannot be used")
            continue

        #check if file exists
        if lineArr[1].strip("\n") not in [item[0] for item in files]:
            print("Write Error: File does not exist")
            audit.write("Write Error: File does not exist\n")
            continue

        file_name_to_search = lineArr[1].strip("\n").strip(" ")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break

        #owner permissions____group permissions______other permissions
        owner = files[index][1]
        fileGroup = files[index][2]
        ownerPermissions = files[index][3]
        groupPermissions = files[index][4]
        otherPermissions = files[index][5]

        inFileGroup = False
        #check if current user is in group specified in file
        for group in groupsAndMembers:
            if str(group[0]) == fileGroup:
                if currentUser in group[1]:
                    inFileGroup = True
                    break

        if(currentUser == "root"):
            print("Write Permission allowed")
            audit.write("Write Permission allowed\n")
        elif(currentUser == owner and "w" in ownerPermissions):
            print("Write Permission allowed")
            audit.write("Write Permission allowed\n")
        elif(currentUser in group and "w" in groupPermissions):
            print("Write Permission allowed")
            audit.write("Write Permission allowed\n")
        elif("w" in otherPermissions):
            print("Write Permission allowed")
            audit.write("Write Permission allowed\n")
        else:
            print("User " + currentUser + " denied write permission for " + lineArr[1].strip("\n"))
            audit.write("User " + currentUser + " denied write permission for " + lineArr[1].strip("\n") + "\n")
            continue

        #append argument to end of file in new line
        with open(file_name_to_search, "a") as f:
            f.write(" ".join(lineArr[2:]))

        print("User: " + currentUser + " added to file: " + lineArr[1] + " with argument: " + lineArr[2].strip("\n"))
        audit.write("User: " + currentUser + " added to file: " + lineArr[1] + " with argument: " + lineArr[2] + "\n")
    #execute
    elif lineArr[0] == "execute":

        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("File names cannot be used")
            continue

        #check if file exists
        if lineArr[1].strip("\n") not in [item[0] for item in files]:
            print("Execute Error: File does not exist")
            audit.write("Execute Error: File does not exist\n")
            continue

        file_name_to_search = lineArr[1].strip("\n")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break

        #owner permissions____group permissions______other permissions
        owner = files[index][1]
        fileGroup = files[index][2]
        ownerPermissions = files[index][3]
        groupPermissions = files[index][4]
        otherPermissions = files[index][5]

        inFileGroup = False
        #check if current user is in group specified in file
        for group in groupsAndMembers:
            if str(group[0]) == fileGroup:
                if currentUser in group[1]:
                    inFileGroup = True
                    break

        if(currentUser == "root"):
            print("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser)
            audit.write("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser + "\n")
        elif(currentUser == owner and "x" in ownerPermissions):
            print("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser)
            audit.write("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser + "\n")
        elif(currentUser in group and "x" in groupPermissions):
            print("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser)
            audit.write("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser + "\n")
        elif(not currentUser in group and "x" in otherPermissions):
            print("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser)
            audit.write("File " + lineArr[1].strip("\n") + " executed sucessfully as: " + currentUser + "\n")
        else:
            print("User " + currentUser + " denied accesss to " + lineArr[1].strip("\n"))
            audit.write("User " + currentUser + " denied accesss to " + lineArr[1].strip("\n") + "\n")

    #ls
    elif lineArr[0] == "ls":

        #disallow file names "accounts.txt, groups.txt, files.txt, and audit.txt"
        if lineArr[1] == "accounts.txt" or lineArr[1] == "groups.txt" or lineArr[1] == "files.txt" or lineArr[1] == "audit.txt":
            print("File names cannot be used")
            continue

        file_name_to_search = lineArr[1].strip("\n")
        for index, item in enumerate(files):
            if item[0] == file_name_to_search:
                break

        owner = files[index][1]
        fileGroup = files[index][2]
        ownerPermissions = files[index][3]
        groupPermissions = files[index][4]
        otherPermissions = files[index][5]

        print(lineArr[1].strip("\n") + ": " + owner + " " + fileGroup + " " + ownerPermissions + " " + groupPermissions + " " + otherPermissions)
        audit.write(lineArr[1].strip("\n") + ": " + owner + " " + fileGroup + " " + ownerPermissions + " " + groupPermissions + " " + otherPermissions + "\n")

    #fallthrough
    else:
        print("Unknown command: " + lineArr[0])


