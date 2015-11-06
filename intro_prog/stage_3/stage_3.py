# Lesson 3.2: Use Functions
# Mini-Project: Take a Break

# Write a program that prompts the user to take a break
# once every two hours, a maximum of three times.

# Your code here.

import time
import webbrowser

total_breaks = 0
break_count = 0

print("This program started on " + time.ctime())
while(break_count < total_breaks):
    time.sleep(3)
    webbrowser.open("www.zalora.com")
    break_count += 1

# Lesson 3.2: Use Functions
# Mini-Project: Secret Message

# Your friend has hidden your keys! To find out where they are,
# you have to remove all numbers from the files in a folder
# called prank. But this will be so tedious to do!
# Get Python to do it for you!

# Your code here.

import os

def rename_files():
    file_list = os.listdir(r"C:\Chris\udacity\intro_prog\stage_3\prank")
    print(file_list)
    os.chdir(r"C:\Chris\udacity\intro_prog\stage_3\prank")
    for file_name in file_list:
        os.rename(file_name, file_name.translate(None, "0123456789"))

rename_files()
