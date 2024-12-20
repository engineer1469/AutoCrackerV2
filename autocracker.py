import glob
import os
import subprocess
import time
import shutil

def set_permissions(file_path):
    try:
        os.chmod(file_path, 0o777)  # Setting read, write, execute permissions for all
    except Exception as e:
        print(f"Error setting permissions for {file_path}: {e}")

def check_permissions(directory):
    try:
        os.listdir(directory)
    except PermissionError:
        print(f"Permission denied: {directory}")
        exit()

def delete_induct_folder(directory):
    induct_path = os.path.join(directory, 'hashcat.induct')
    if os.path.isfile(induct_path):
        try:
            print(f"Setting permissions for induct file: {induct_path}")
            set_permissions(induct_path)
            os.remove(induct_path)
            print(f"Deleted induct file: {induct_path}")
        except Exception as e:
            print(f"Error deleting induct file: {e}")
    elif os.path.isdir(induct_path):
        try:
            print(f"Setting permissions for induct folder: {induct_path}")
            set_permissions(induct_path)
            shutil.rmtree(induct_path)
            print(f"Deleted induct folder: {induct_path}")
        except Exception as e:
            print(f"Error deleting induct folder: {e}")

def crack():
    Dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(Dir)
    handshakes = glob.glob(str(Dir) + "/handshakes/*")

    a = input("Do you want to enable brute-force attacks? (~+5min) Y or N: ")
    if a.lower() == "y":
        brute_force = True
    elif a.lower() == "n":
        brute_force = False
    else:
        print(f"{a} is not a valid input")
        exit()

    hashcat_dir = os.path.join(Dir, "hashcat-6.2.6")
    check_permissions(hashcat_dir)

    for handshake in handshakes:
        delete_induct_folder(hashcat_dir)
        time.sleep(2)  # Sleep for 2 seconds to allow hashcat to clean up

        os.chdir(hashcat_dir)
        command = f"{hashcat_dir}\\hashcat.exe -w 4 -m 22000 {handshake} -a 0 pass.txt"
        result = os.system(command)

        if result == 1 and brute_force:
            os.system(f"{hashcat_dir}\\hashcat.exe -w 4 -m 22000 {handshake} -a 3 ?d?d?d?d?d?d?d?d")

    for handshake in handshakes:
        os.system(f"{hashcat_dir}\\hashcat.exe -w 4 -m 22000 {handshake} -a 0 pass.txt --show")

if __name__ == "__main__":
    crack()
