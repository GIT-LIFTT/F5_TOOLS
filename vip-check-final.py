import paramiko
import time
import csv


username = input("please enter username")
password = input("please enter password")
ip_address = input("please enter the ip address")

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address, username=username, password=password)

print("please enter vs list in the following format server1_vs,server2_vs,server3_vs")
# get input from the user and store it in the varible vslist
vslist = input()

#take the vslist  splits a string into a list.
vslist1 = vslist.split(",")

# create a dictionary
dict={}

# iterate through the list of virtual servers
for a in vslist1:

 #create a the command with the name of the virtual server for each time the lopp iterates
 cmd = ("show /ltm virtual "+a)

 # using method 2 of passing commands to the paramiko shell
 # high level assigns  standard input standard output and standard error to the output paramiko shell
 stdin, stdout, stderr = ssh_client.exec_command(cmd)
 time.sleep(2)

 #assings the output of readlines to standard output
 # the following command will output only what is returned by the command
 stdout = stdout.readlines()

#THE OTHER METHOD FOR EXTRACTING DATA FROM THE OUTPUT
#remote_connection.send("show config\n")
#remote_connection.send("end\n")
#output = remote_connection.recv(1000)


 #assigned the current virtual server name to the varible current
 current = a

 # for loop to iterate through the elments within the  output from the command we sent
 for i in stdout:
     # if the string "State" is matched in i which is iterating through the elements in the output from the command
     if ("State" in i):
        # assign the value of i to b after we have replaced "State            " with "State: "
        b = i.replace('State            :','State: ')

     # else if Availability is matched
     elif ("Availability" in i):

        # assing i to c after we have replaced "Availability     :" with "Availability: "
        c = i.replace ('Availability     :','Availability: ')

 #create a dictionary using the the varible current  ans the key (the virtual server name ) and assign both the values
 # of c and b as values to the key
 dict[(current)] = c,b

# create a list using the keys from the dictionary dict using the .keys() method
keys = list(dict.keys())


# opens a new file
with open('dict-to-csv.csv', mode='w', newline='') as csv_file:


    # creates a list with the following values
    fieldnames = ['ID', 'status', 'availability']

    # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # Create an object which operates like a regular writer but maps dictionaries onto output rows.
    # The fieldnames parameter is a sequence of keys that identify the order in which values in the
    # dictionary passed to the writerow() method are written to file f
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # writes the headers
    # Write a row with the field names (as specified in the constructor).
    writer.writeheader()

    # as we defined earlier a list  of the keys from the opriginal dictionary
    # this allows us to iterate through each key : value pair
    # for k in the range of keys see above = 2
    for k in range(len(keys)):
        status = "none"
        availability = "none"

        #  a for loop within a for loop  allows us to iterate through the elements within the current keY
        for i in (dict[keys[k]]):

            #if the string State is matched is matched in i
            if ("State" in i):

                # b = i with State removed so we go from "State:  enabled" to  "enabled"
                # this is so when we are building the rows in excel we only have the value where as the header for the colume
                # shows what the value means as shown below
                # State
                # enabled
                b = i.replace('State:', '')

                #finally strip all empty space from the remaning value so we should just be left with the actual value enabled
                b = b.strip()

                #assign the value of b to status
                status = b

            # see above repeated below for  Availability
            elif ("Availability" in i):
                c = i.replace('Availability:', '')
                c = c.strip()
                availability = c

        # write a row with the current values of the varibles within the given for loop
        writer.writerow(
            {'ID': keys[k], 'status': status, 'availability': availability})
ssh_client.close