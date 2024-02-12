import socket
import sys

def conn_handler(conn, addr):
    print("Connected with ", addr[0])
    a.append([addr[0], addr[1]])
    while True:
        try:
            msg = input('Message to send to client : ')
            if msg == "exit":
                print("closing the connection")
                conn_out(conn, msg)
                conn.close()
                break
            conn_out(conn, msg)
            res = conn_in(conn)
            if res == 'exit':
                print('client closed connection')
                conn.close()
                break
            print('response from client : ', res)
        except KeyboardInterrupt:
            print('\n keyboard interrupt issued')
            msg = "exit"
            conn_out(conn, msg)
            conn.close()
            break
        except Exception:
            conn.close()
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
    conn,addr = sock.accept()
    conn_handler(conn, addr)

if __name__=='__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a = []
    try:
        host_ip=sys.argv[1]
        host_port=int(sys.argv[2])
        listner_handler()
    except IndexError:
        print("\n Missing arguments")
    except Exception as e:
        print("\n")
        print(e)







    