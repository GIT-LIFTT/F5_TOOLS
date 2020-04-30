import paramiko
import time
import csv

username = input("please enter username")
password = input("please enter password")
ip_address = input("please enter the ip address")

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_address, username=username, password=password)

# read list in
with open('vs') as f:
    vslist1 = f.read().splitlines()

# ensure the correct number of virtual servers have been read in from the file
# x is equal to the len of vslist1
x = len(vslist1)
print(x, " servers read from the file ")
print("press any key to continue")
# using this to pause for any input and control the flow of the program
input()

# enter the name of the old cert we are removing
oldclientsslprofile = input("please enter the name of the old client ssl profile")
newclientsslprofile = input("please eneter the name of the new client ssl profile")

# for loop the list
for i in vslist1:

    # send this command and store the result to a varible for string matching
    # send the following command to ensure the virtual server we have has the correct cert configured before we remove
    cmd1 = ("list ltm virtual " + i + " one-line ")
    print(cmd1)
    stdin, stdout, stderr = ssh_client.exec_command(cmd1)
    output = stdout.readlines()
    # if the the current server has the cert perform the following
    OUTPUTasSTRING = ""
    OUTPUTasSTRING = OUTPUTasSTRING.join(output)
    if (oldclientsslprofile in OUTPUTasSTRING):
        print("cert found in ", i)
        time.sleep(2)

        # print modify cert for X
        print("deleting " + oldclientsslprofile + " from ", i)
        cmd2 = ("modify ltm virtual " + i + " profiles delete { " + oldclientsslprofile + " }")
        # remove old cert
        stdin, stdout, stderr = ssh_client.exec_command(cmd2)
        time.sleep(1)
        # add new cert
        print("adding " + newclientsslprofile + " to ", i)
        time.sleep(1)
        cmd3 = ("modify ltm virtual " + i + " profiles add { " + newclientsslprofile + " }")
        stdin, stdout, stderr = ssh_client.exec_command(cmd3)
        error = stderr.readlines()
        print(error)
        print("============================")
    elif (oldclientsslprofile not in OUTPUTasSTRING):
        print("cert not found in ", i)
        print("============================")

# create a dictionary
dict = {}

for i in vslist1:
    # initialise the varible which represents the current cert to be "no cert"
    # that way if the desired cert is not found the varible is not change and this it is highlighted in the spreadsheet with "no cert
    currentcert = "new cert not found"
    # build the command
    cmd1 = ("list ltm virtual " + i + " one-line ")
    # run the command
    stdin, stdout, stderr = ssh_client.exec_command(cmd1)

    # read the output to the varible output
    # !!! the output comes in the form of a list
    output = stdout.readlines()

    # create a varible which will hold the converted list as a string
    OUTPUTasSTRING = ""
    # convert the list to a string
    OUTPUTasSTRING = OUTPUTasSTRING.join(output)
    # if the new cert is found  in the configuration of the virtual server
    if (newclientsslprofile in OUTPUTasSTRING):
        # change the value of currentcert to that of newclinetsslprofile as that was the string which was matched in the config
        currentcert = newclientsslprofile

    # create  dictionary and populate with virtual server name and cert
    dict[(i)] = [currentcert]
# create a list using the keys from the dictionary dict using the .keys() method


keys = list(dict.keys())

# write rows

with open('cert-change-output.csv', mode='w', newline='') as csv_file:
    # creates a list with the following values
    fieldnames = ['virtualserver', 'clientsslprofile']

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
        # print(keys[k])
        clientsslprofile = "failed"
        time.sleep(1)
        #  a for loop within a for loop  allows us to iterate through the elements within the current key
        # for i in (dict[keys[k]]):
        # if string value which = clientsslprofile is found assing to the varible i
        # if ("iteration" in i):
        # status = i

        # elif ("iteration" in i):
        # availability = i
        for i in (dict[keys[k]]):

            if (newclientsslprofile in i):

                b = i.strip()

                clientsslprofile = b
                # print("this is the output State :", current, ": ", b)
            ####
            elif ("new cert not found" in i):

                b = i.strip()
                clientsslprofile = b

        # write a row with the current values of the varibles within the given for loop
        writer.writerow(
            {'virtualserver': keys[k], 'clientsslprofile': clientsslprofile})