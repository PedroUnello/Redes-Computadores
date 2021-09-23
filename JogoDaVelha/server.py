import socket
from _thread import *
import sys

server = "192.168.15.5"
port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)

print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return [(int(str[0]), int(str[1])),int(str[2]),int(str[3]),str[4]]


def make_pos(tup):
    return str(tup[0][0]) + "," + str(tup[0][1]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

#pos = [[(0,0),0],[(0,0),1]]
pos = [[(0,0),0,0,"c"],[(0,0),1,0,"c"]]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Received: ", data)
                print("Sending : ", reply)
                #print(pos)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    try:
        ip = addr[0]
        print("Connectado à:",socket.gethostbyaddr(str(ip))[0],"\nIp: ", addr)
    except:
        print("Erro pegando nome de conexão")
    if currentPlayer > 1:
        currentPlayer = 0
        pos = [[(0, 0), 0, 0, "c"], [(0, 0), 1, 0, "c"]]
    if currentPlayer == 1:
        print('Começando novo jogo!\n\n')
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
