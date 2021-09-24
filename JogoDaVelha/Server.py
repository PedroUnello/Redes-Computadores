import socket
from _thread import *
import re

def read_data(str):
    strL = str.split(",")
    if len(strL) > 2:
        return [(int(strL[0]), int(strL[1])),int(strL[2]),int(strL[3]),strL[4]]
    return [strL[0], int(strL[1])]

def make_data(tup):
    return str(tup[0][0]) + "," + str(tup[0][1]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

def manipulate_score(nome, pontuação):
    existente = False
    placarGeral = open("placar.txt","r") #abre o placar
    textoL = placarGeral.read().splitlines()
    placarGeral.close()
    placarGeral = open("placar.txt","w")
    searchPatter = re.compile("^" + str(nome) + ".*[0-9]$") #Procura se o nome já existe com regex
    for i in range(len(textoL)): #Incrementa e/ou coloca a pontuação daquele nome
        if re.match(searchPatter, textoL[i]):
            existente = True
            pontuação += int(re.findall(".[0-9][0-9]$",textoL[i])[0])  
            textoL[i] = searchPatter.sub(str(nome) + " - " + str(pontuação), textoL[i]) 
            print(textoL[i])                     
    if not existente:
        textoL.append(str(nome) + " - " + str(pontuação))
        print(textoL[i]) 
    textoL = "\n".join(textoL)    
    placarGeral.write(textoL)
    placarGeral.close()
    return True

data = [[(0,0),0,1,"c"],[(0,0),1,0,"c"]]
currentPlayer = 0

server = "192.168.15.5"
port = 41929

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    str(e)
s.listen(2)
print("Servidor Iniciado")

def threaded_client(conn, player):
    conn.send(str.encode(make_data(data[player]))) #Envia os dados do servidor para o cliente, quando este conecta
    while True:
        try:    #Funcionamento p/ cada player -> Recebe os dados de tal player, e manda os do oponente

            rData = read_data(conn.recv(2048).decode()) #Sempre lê os dados deste player
            
            if len(rData) == 2: #Acabou o jogo
                manipulate_score(rData[0],rData[1])
                break

            if player == 1: #Prepara uma resposta para o jogador oposto
                    reply = 0
            else:
                    reply = 1
            
            if data[player] != rData: #Se receber um estado diferente do cliente
                
                print("Received: {} from: {} ".format(rData, data[player][3]))
                print("Sending : {} to: {}".format(data[reply], data[player][3]))

            data[player] = rData #Altera o ultimo estado do servidor

            if not rData: #Se não receber, caiu
                print("Disconnected")
                break
            
            conn.sendall(str.encode(make_data(data[reply]))) #Sempre envia o estado atual do oponente para este player

        except:
            break

    print("Lost connection") #Se cair na excessão de acima ou cair a conexão (não recebeu dados), fecha o socket
    conn.close()

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
