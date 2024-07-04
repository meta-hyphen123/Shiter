import os
import sys
import time
import threading
import importlib
import subprocess
import getpass
import keyboard

# Libraries to check and install if missing
libraries = [
    'os', 'time', 'subprocess', 'fade', 'random', 'glob',
    'getpass', 'requests', 'webbrowser', 'sys', 'json',
    'shutil', 'threading', 'colorama', 'keyboard'
]

# Check and install missing libraries
def check_and_install_libraries(libs):
    not_installed = []
    for lib in libs:
        try:
            importlib.import_module(lib)
        except ImportError:
            not_installed.append(lib)
    
    if not_installed:
        print(f"Installing missing libraries: {', '.join(not_installed)}")
        for lib in not_installed:
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        print("All libraries installed successfully.")
    else:
        print("All libraries are installed.")

check_and_install_libraries(libraries)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def write_to_text_file(file_path, text):
    try:
        with open(file_path, 'w') as file:
            file.write(text)
    except FileNotFoundError:
        print("File not found!")

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print("File not found!")
        return None

def replace_url(url):
    name = url.replace("https://github.com/meta-hyphen123/", "")
    print(name)
    write_to_text_file(I, name)

clone_complete = False

def moving_block(total_length=60, block_length=30, speed=0.0001):
    global clone_complete
    start_time = None
    try:
        while not clone_complete:
            for position in range(total_length + block_length):
                if clone_complete:
                    break
                bar = [" "] * total_length
                for i in range(block_length):
                    if 0 <= position - i < total_length:
                        bar[position - i] = "━"
                sys.stdout.write("\r      " + "".join(bar))
                sys.stdout.flush()
                time.sleep(speed)

                if keyboard.is_pressed('u'):
                    if start_time is None:
                        start_time = time.time()
                    elif time.time() - start_time >= 2:
                        print("\nUpdate triggered.")
                        return
                else:
                    start_time = None
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()

def moving_blockA(total_length=60, block_length=30, speed=0.0001):
    global clone_complete
    start_time = None
    try:
        for _ in range(3):
            for position in range(total_length + block_length):
                if clone_complete:
                    break
                bar = [" "] * total_length
                for i in range(block_length):
                    if 0 <= position - i < total_length:
                        bar[position - i] = "━"
                sys.stdout.write("\r      " + "".join(bar))
                sys.stdout.flush()
                time.sleep(speed)

                if keyboard.is_pressed('u'):
                    if start_time is None:
                        start_time = time.time()
                    elif time.time() - start_time >= 2:
                        print("\nUpdate triggered.")
                        return
                else:
                    start_time = None
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        sys.stdout.flush()

def clone_repo():
    result = os.system("git clone https://github.com/meta-hyphen123/version")
    if result != 0:
        print("Failed to clone the version repository.")
        return False

    if not os.path.exists("version"):
        print("The version directory does not exist.")
        return False

    os.chdir("version")
    ver = os.path.join(os.getcwd(), 'version.txt')
    url = read_text_file(ver)
    os.chdir("..")
    result = os.system(f"git clone {url}")
    if result != 0:
        print("Failed to clone the Shiter repository.")
        return False

    replace_url(url)
    return True

def install_shiter():
    global clone_complete
    clone_complete = False

    progress_thread = threading.Thread(target=moving_block)
    progress_thread.start()

    success = clone_repo()

    clone_complete = True
    progress_thread.join()

    if success:
        print("\nClone complete!")
    else:
        print("\nClone failed!")

logo = """
                                 ▄████████ 
                                ███    ███ 
                                ███    █▀  
                                ███        
                              ▀███████████ 
                                       ███ 
                                 ▄█    ███ 
                               ▄████████▀  
                                           
"""

print(logo)

current_file_path = os.path.dirname(os.path.abspath(__file__))
I = os.path.join(current_file_path, 'data', 'version.txt')

def update_shiter():
    print("\n       If you try to update it, you might lose all your data in Shiter")
    y_or_n = input("[yes or no] ")
    if y_or_n.lower() == 'yes':
        install_shiter()

def login(password, shiter):
    clear()
    print(logo)
    pdw = getpass.getpass("Password for Shiter: ")
    if pdw == password:
        clear()
        print(logo)
        print("                           Welcome To Shiter!")
        moving_blockA()
        os.chdir(shiter)
        print()
        os.system("python3 shiter.py")
    else:
        login(password, shiter)

def create_password(password_file):
    print(logo)
    pdw = getpass.getpass("Please create a password for Shiter: ")
    Apdw = getpass.getpass("Please verify the password for Shiter: ")
    if pdw == Apdw:
        write_to_text_file(password_file, pdw)
    else:
        create_password(password_file)

if __name__ == "__main__":
    moving_blockA()
    password_file = os.path.join(current_file_path, 'data', 'password.txt')
    password = read_text_file(password_file)
    clear()
    if not password:
        create_password(password_file)
    else:
        version = read_text_file(I)
        if not version:
            install_shiter()
        else:
            shiter_path = os.path.join(current_file_path, version)
            if 'shiter' in version.lower():
                login(password, shiter_path)
            else:
                print("WTF?")
