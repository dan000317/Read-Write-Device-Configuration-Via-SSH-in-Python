import os.path
import sys

# Checking if IP address file and its content validity
def ip_file_valid():

    # Prompting user for input
    ip_file = input ("\n# Enter IP file path and name (e.g., D:\MyApps\myfile.txt or /home/user1/MyApps/myfile.txt):    ")

    # Checking if the file exists
    if os.path.isfile(ip_file) == True:
        print("\nIP file is valid\n")
    
    else:
        print ("\nFile {} does not exists. Please check and try again.\n".format(ip_file))
        sys.exit
    
    # Open user selected file for reading (IP address file)
    selected_ip_file = open(ip_file, 'r')

    # Starting from the line at the beginning of the file, read each IP address
    selected_ip_file.seek(0)
    ip_list = selected_ip_file.readlines()

    # Closing the file
    selected_ip_file.close()
    
    return ip_list