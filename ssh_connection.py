import paramiko
import os.path
import time
import sys
import re

# Checking username/password file
# Prompting user for input - USERNAME/PASSWORD File
user_file = input("\nEnter userdata file path and name (e.g., D:\MyApps\myfile.txt or /home/user1/MyApps/myfile.txt):    ")

# Verify the validity of the USERNAME/PASSWORD File
if os.path.isfile(user_file) == True:
    print ("\n Username/Password file is valid \n")

else:
    print("\n File {} does not exist. Please check and try again".format(user_file))
    sys.exit

# Checking command file
# Prompting user for input - COMMANDS File
cmd_file = input("\nEnter commands file path and name (e.g., D:\MyApps\myfile.txt or /home/user1/MyApps/myfile.txt):    ")

# Verifying the validity of the COMMANDS File
if os.path.isfile(cmd_file) == True:
    print ("\n  Commands File is valid.")

else:
    print("\n File {} does not exist. Please check and try again".format(cmd_file))
    sys.exit

#Open SSHv2 connection to the device
def ssh_connection(ip):
    global user_file
    global cmd_file

    # Creating SSH Connection 
    #### Securely store SSH paramters ####
    try:
        # Define SSH parameters
        selected_user_file = open (user_file, 'r')

        # Reading the username from the file starting from the beginning
        selected_user_file.seek(0)
        username = selected_user_file.readlines()[0].split(',')[0].rstrip('\n')

        # Reading the password from the file starting from the beginning
        selected_user_file.seek(0)
        password = selected_user_file.readlines()[0].split(',')[1].rstrip('\n')

        # Logging into device
        session = paramiko.SSHClient()

        # For Testing purposes, this allows auto-accepting unknown host keys
        # Do not use in production! The default would be RejectPolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Secure Connection requires the following variables:
        #   username = "<Insert your ssh user here>" - already declared in user.txt
        #   password = "<Insert your ssh password here>" - already declared in user.txt
        #   ip = "<Insert the IP/host of your device/server here>" - already declared in ip-file.txt
        ##### Suggested edits: Secure the user credentials #####
        #   ssh_port = 22 # Change this if your SSH port is different
        
        # session.load_system_host_keys()
        # try:
        #    session.connect(ip, port=ssh_port,
        #                        username=username,
        #                        password=password,
        #                        look_for_keys=False)
        #    print("Connected Successfully!")
        #
        # except Exception:
        #    print ("Failed to establish connection.")

        # Connect to the device using username and password
        session.connect(ip.rstrip('\n'), username=username, password=password)

        # Start an interactive shell session
        connection = session.invoke_shell()

        # Setting terminal length for entire output - disable pagination
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)

        # Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)

        # Open user selected file for reading
        selected_cmd_file = open(cmd_file,"r")

        # Starting from the beginning of the file, write each line to the device
        selected_cmd_file.seek(0)
        for each_line in selected_cmd_file.readlines():
            connection.send(each_line + "\n")
            time.sleep(2)
        
        # Closing the userfile
        selected_user_file.close()

        # Closing the command file
        selected_cmd_file.close()

        # Checking command output for IOS syntax errors
        router_output = connection.recv(65535)
        if re.search(b"% Invalid input", router_output):
            print("\nThere was at least one IOS syntax error on device".format(ip))

        else:
            print("\nDone for device {}".format(ip))

        # Test for reading command output
        print(str(router_output) + "\n")

        # Closing the connection
        session.close()

    except paramiko.AuthenticationException:
        print("\nInvalid username or password! Please check user.txt file and the device configuration")
        print("\nClosing the program")
