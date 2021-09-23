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

def read_data(str):
    str = str.split(",")
    return [(int(str[0]), int(str[1])),int(str[2]),int(str[3]),str[4]]


def make_data(tup):
    return str(tup[0][0]) + "," + str(tup[0][1]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

#data = [[(0,0),0],[(0,0),1]]
data = [[(0,0),0,0,"c"],[(0,0),1,0,"c"]]

def threaded_client(conn, player):
    conn.send(str.encode(make_data(data[player]))) #Envia os dados do servidor para o cliente, quando este conecta
    while True:
        try:    #Funcionamento p/ cada player -> Recebe os dados de tal player, e manda os do oponente

            rData = read_data(conn.recv(2048).decode()) #Sempre lê os dados deste player
            data[player] = rData #Altera o ultimo estado do servidor
            if not rData: #Se não receber, caiu
                print("Disconnected")
                break
            if player == 1: #Prepara uma resposta para o jogador oposto
                    reply = 0
            else:
                    reply = 1
            
            
            if data[reply] != rData: #Se receber um estado diferente do cliente
                
                print("Received: {} from: {} ".format(rData, data[player][3]))
                print("Sending : {} from: {}".format(data[reply], data[player][3]))

            conn.sendall(str.encode(make_data(data[reply]))) #Sempre envia o estado atual do oponente para este player
        except:
            break

    print("Lost connection") #Se cair na excessão de acima ou cair a conexão (não recebeu dados), fecha o socket
    conn.close()

currentPlayer = 0


while True:
    conn, addr = s.accept()
    try:
        ip = addr[0]
        print("Connectado à:", conn.gethostbyaddr(str(ip))[0],"\nIp: ", addr)
    except:
        print("Erro pegando nome de conexão")
    if currentPlayer > 1:
        currentPlayer = 0
        data = [[(0, 0), 0, 0, "c"], [(0, 0), 1, 0, "c"]]
    if currentPlayer == 1:
        print('Começando novo jogo!\n\n')
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
