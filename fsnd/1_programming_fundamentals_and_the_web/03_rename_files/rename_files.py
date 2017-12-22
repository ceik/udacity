import os

def rename_files():
    file_list = os.listdir(r"/home/ceik/github/udacity/fsnd/1_programming_fundamentals_and_the_web/3_rename_files")
    print(file_list)

    for file in file_list:
    	os.rename(file, file.translate(None, "0123456789"))

rename_files()