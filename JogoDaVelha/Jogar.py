import pygame as pg
import re
import random
import sys
import socket

caminhoParaPasta = "/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/"

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cria um atributo client, utilizando o prot TCP
        self.server = "192.168.15.5" #Ip a conectar (servidor)
        self.port = 5000 #Porta de conexão
        self.addr = (self.server, self.port) #cria o endereço
        self.data = self.connect() #chama o método local para conectar, para tratar erros de conexão em uma excessão,
                                  # self.data são os dados recebidos na conexão com o servidor, data=dados de posição/jogada no jogo

    def connect(self):
        try:
            self.client.connect(self.addr) #Conecta ao endereço criado no construtor, utilizando do three-way-handshake
            return self.client.recv(2048).decode() #Recebe e retorna os dados pelo recv(), que é referente ao TCP
        except socket.error as e:
            print(e) #Printa o erro no terminal do jogo

    def send(self, data): #
        try:
            self.client.send(str.encode(data)) #Faz o encode para utf-8, e manda pelo socket criado da instância
            return self.client.recv(2048).decode() #Similar ao connect
        except socket.error as e:
            print(e)

class Jogador():
    valido = False
    def __init__(self, Nome, Pontuação, Lado):
        self.Nome = Nome
        self.Pontuação = Pontuação
        self.Lado = Lado

    def Jogar(self, pos,colliders):
        for i in range(len(colliders)):
            if colliders[i].collidepoint(pos[0],pos[1]):
                posMatriz = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
                posMatriz = posMatriz[i]
                if tabuleiro.matriz[posMatriz[0]][posMatriz[1]] != "X" and tabuleiro.matriz[posMatriz[0]][posMatriz[1]] != "O":
                    tabuleiro.CriarPontos(self.Lado[0], posMatriz)
                    Ijogada = pg.image.load(str(self.Lado[1]))
                    screen.blit(Ijogada,(colliders[i][0]+10,colliders[i][1]-10))
                    print(tabuleiro.matriz)
                    self.valido = True
                else:
                    self.valido = False

    def Voltar(self):
        print("Jogador", self.Nome, "Voltou")

    def Desistir(self):
        print("Jogador", self.Nome, "Desistiu")

class Botão():

    def __init__(self,Imagem,Posição,Nome,Ação):
        self.Imagem = Imagem
        self.Posição = Posição
        self.Nome = Nome
        self.Ação = Ação

    def Ação(self):
        self.Ação

    def __delete__(self):
        del self

class Tabuleiro():
    
    def __init__(self):
        self.matriz = [[0,0,0],[0,0,0],[0,0,0]]
        self.Imagem = pg.image.load(caminhoParaPasta + "img/" + "Tabu1.png")
        self.ganhador = False
        self.finalizado = False

    def CriarPontos(self,lado,pos):
        if lado != None:
            self.matriz[pos[0]][pos[1]] = lado

    def Status(self):
        contDiagP, contDiagS = ["","",""],["","",""]
        
        for i in range(len(self.matriz)):
            contLin,contCol = ["","",""],["","",""]

            if self.matriz[i][i] == "X":
                contDiagP[i] = "X"
            elif self.matriz[i][i] == "O":
                contDiagP[i] = "O"

            if self.matriz[i][2-i] == "X":
                contDiagS[i] = "X"
            elif self.matriz[i][2-i] == "O":
                contDiagS[i] = "O"
            
            for j in range(len(self.matriz[i])):
                if self.matriz[i][j] == "X":
                    contLin[j] = "X"
                elif self.matriz[i][j] == "O":
                    contLin[j] = "O"
                if self.matriz[j][i] == "X":
                    contCol[j] = "X"
                elif self.matriz[j][i] == "O":
                    contCol[j] = "O"
                    
            if contLin == ["X","X","X"] or contCol == ["X","X","X"] or contDiagS == ["X","X","X"] or contDiagP == ["X","X","X"]:
                self.finalizado = True
                self.ganhador = "X"
            if contLin == ["O","O","O"] or contCol == ["O","O","O"] or contDiagS == ["O","O","O"] or contDiagP == ["O","O","O"]:
                self.finalizado = True
                self.ganhador = "O"

def read_data(str): #Lê os dados recebidos no servidor
    str = str.split(",")
    return [(int(str[0]), int(str[1])),int(str[2]),int(str[3]),str[4]]

def make_data(tup): #Faz os dados para enviar pelo servidor
    return str(tup[0][0]) + "," + str(tup[0][1]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

def CompararPosição(Mouse, Posição, Tamanho): #Facilidade de uso por encapsulamento da verificação
    return Mouse[1]>=Posição[1] and Mouse[1] <= Posição[1] + Tamanho[1] and Mouse[0] >= Posição[0] and Mouse[0] <= Posição[0] + Tamanho[0]

def ImprimirVisual(texto, fonte = None, tamanho = None, alturaInicial = None, posiçãoInicial = None, espaço = None, limite = None, cor = None):
    fonte = fonte or "Helvetiva"
    tamanho = tamanho or 30
    alturaInicial = alturaInicial or 15
    posiçãoInicial = posiçãoInicial or False
    espaço = espaço or 15
    limite = limite or len(texto)
    cor = cor or (0,0,255)
    fonteTexto = pg.font.SysFont(fonte,tamanho)
    alturaT = alturaInicial
    if limite > len(texto):
        limite = len(texto)
    for index in range(limite):
        if posiçãoInicial == False:
            larguraT = fonteTexto.size(texto[index])[0]
            larguraDinamica = (largura//2) - (larguraT//2)
        else:
            larguraDinamica = posiçãoInicial
        tImprimir = fonteTexto.render(texto[index], True, cor)
        screen.blit(tImprimir, [larguraDinamica,alturaT])
        alturaT += espaço


pg.init()
largura = 1000
altura = 1000
screen = pg.display.set_mode((largura, altura))
pg.display.set_caption("Jogo da Velha -Sockets-")
screen.fill((0,0,0))
pg.display.flip()

enter, criando, pronto, jogando = False, False, False, False
lado,userInput = ["X","O"], ['']
contTurno = 0
pos = (0,0)

slots = [(400,430),(500,430),(600,430),(400,520),(500,520),(600,520),(400,610),(500,610),(600,610)]
colliders = [0] * 9
for i in range(9):
    colliders[i] = pg.Rect(slots[i], (85, 95))

tabuleiro = Tabuleiro()
Jog2, Jog1 = None, None

while True:

    for event in pg.event.get():

        if event.type == pg.MOUSEBUTTONDOWN: #Só pega os inputs do mouse
            if jogando: #Se tiver jogando
                if f[1]%2 == contTurno%2: #e o primeiro dado da leitura do servidor for igual a contagem de turnos (modulo para ver a vez)
                    if pg.mouse.get_pressed()[0]:
                        pos = pg.mouse.get_pos()
                        print(pos)
                else:
                    pass
            else:
                if pg.mouse.get_pressed()[0] and not (CompararPosição(pos, BotãoMulti.Posição, (90,30))):
                    pos = pg.mouse.get_pos()
                    print(pos)


        if event.type == pg.KEYDOWN: #Input de texto (nomes, etc) | nessa versão só pra nomes
            if criando:
                if event.key == pg.K_RETURN:
                    enter = True
                elif event.key == pg.K_BACKSPACE:
                    userInput[0] = userInput[0][:-1]
                    pg.draw.rect(screen,(0,0,0),(50,50,tLargura,31))
                elif len(userInput[0]) < 20:
                    userInput[0] += event.unicode
            
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if not jogando: #Cria a tela inicial
        screen.blit(tabuleiro.Imagem,(0,0))
        barraCriacao = pg.Rect(50,50,90,30)
        corA = (0,255,0)
        BotãoMulti = Botão(pg.image.load(caminhoParaPasta + "img/" + "Botão4.png"),(500,300),["Multi"],"PlaceHolder")
        screen.blit(BotãoMulti.Imagem,BotãoMulti.Posição)
        ImprimirVisual(BotãoMulti.Nome,None,None,BotãoMulti.Posição[1]+15,BotãoMulti.Posição[0]+40)

    if criando and not enter: #Caso esteja na tela de preencher nome, ajusta a fonte, e aumenta o tamanho da barra de input caso necessário
        text = font.render(userInput[0], True, corA)
        tLargura = max(200,text.get_width() +10)
        barraCriacao.w = tLargura
        pg.draw.rect(screen,(0,0,0),barraCriacao)
        screen.blit(text, (barraCriacao.x+5, barraCriacao.y+5))
        pg.draw.rect(screen, corA, barraCriacao, 2)

    if criando and enter: #Formata a entrada, e coloca o nome dado para o jogador atual
        userInput[0] = userInput[0].lower()
        userInput[0] = userInput[0][0].upper() + userInput[0][1:]
        pg.draw.rect(screen,(0,0,0),(50,50,90,30))#Remover
        if Jog1 == None:
            Jog1 = Jogador(userInput[0],0,["X",caminhoParaPasta + "img/" + "X1.png"])
        elif Jog2 == None:
            Jog2 = Jogador(userInput[0],0,["O",caminhoParaPasta + "img/" + "O1.png"])
        userInput = ['']
        criando = False
        
    listaJogadores = [Jog1,Jog2]  
    
    if CompararPosição(pos, BotãoMulti.Posição, BotãoMulti.Imagem.get_rect().size) and not jogando:
        
        if Jog1 == None: #Se ainda não tem jogador, abre a barra de criação
            font = pg.font.Font(None, 32)
            criando = True
        else: #Terminado de criar, abre a conexão com o servidor para matchmaking
            n = Network()
            f = read_data(n.data)
            Jog2 = Jogador("",0,["O",caminhoParaPasta + "img/" + "O1.png"])
            pronto = True
            recompensa = 20
        pg.display.flip()

        if pronto:
            placarGeral = open("placar.txt","r")
            texto = placarGeral.read()
            textoL = texto.splitlines()
            placarGeral.close()
            for i in range(len(textoL)):
                if re.match("\A" + str(Jog1.Nome), textoL[i]):
                    Jog1.Pontuação = int(re.findall(".[0-9][0-9]$",textoL[i])[0])
            pos = (0,0)
            screen.blit(tabuleiro.Imagem,(0,0))
            jogando = True
            
    if jogando:

        ImprimirVisual(["Vez de"],alturaInicial=310,posiçãoInicial=535,cor = (0,0,0))
        pg.draw.line(screen,(100,0,0),(460,300),(500,340),3) #X
        pg.draw.line(screen,(100,0,0),(500,300),(460,340),3) 
        pg.draw.circle(screen,(0,0,100),(650,310),20,3) #O
        if lado[contTurno%2] == "X": #Desenha novamente, só que mais claro para demonstrar o turno
            pg.draw.line(screen,(255,0,0),(460,300),(500,340),3)
            pg.draw.line(screen,(255,0,0),(500,300),(460,340),3)
        elif lado[contTurno%2] == "O":
            pg.draw.circle(screen,(0,0,255),(650,310),20,3)
                
        hold = read_data(n.send(make_data([pos,contTurno,1,Jog1.Nome]))) #Mandando a atual, recebe a do oponente
        if hold[2] != 0: #Controla a jogada pela vez -> dada nos dados sincronizados do servidor
            Jog2.Nome = hold[3]
            for i in range(len(textoL)):
                if re.match("\A" + str(Jog2.Nome), textoL[i]):
                    Jog2.Pontuação = int(re.findall(".[0-9][0-9]$",textoL[i])[0])
            jogadorAtual = listaJogadores[hold[1]%2] #jogadorAtual -> oponente (sincroniza pelo servidor)
            jogadorAtual.Jogar(hold[0],colliders) #Joga pelo jogador atual (oponente) utilizando os dados do mouse, sincronizados no servidor
            jogadorAtual = listaJogadores[contTurno%2] #jogadorAtual -> player
            jogadorAtual.Jogar(pos,colliders) #Tenta jogar na ultima posição de clique, ou seja, joga quando o ultimo clique for valido
            if jogadorAtual.valido: #Se a jogada for valida
                if f[1] % 2 == 0: #Faz a jogada e reseta as variaveis e atributos
                    ImprimirVisual([Jog1.Nome], alturaInicial=265, posiçãoInicial=450, cor=(0, 0, 0))
                    ImprimirVisual([Jog2.Nome], alturaInicial=265, posiçãoInicial=620, cor=(0, 0, 0))
                else:
                    ImprimirVisual([Jog2.Nome], alturaInicial=265, posiçãoInicial=450, cor=(0, 0, 0))
                    ImprimirVisual([Jog1.Nome], alturaInicial=265, posiçãoInicial=620, cor=(0, 0, 0))
                contTurno +=1
                jogadorAtual.valido = False
                jogadorAtual = None
                pos = (0,0)
                tabuleiro.Status() #Checa se o jogo acabou/alguem ganhou
                pg.display.flip()
            
    if tabuleiro.finalizado or contTurno == 9: #Se acabar o jogo

        if tabuleiro.finalizado: #Caso alguem tenha ganho
            pg.time.delay(2000)
            screen.fill((0,0,0)) #Prepara a tela
            backGround = pg.image.load(caminhoParaPasta + "img/" + "BackGround.jpeg")
            premio = pg.image.load(caminhoParaPasta + "img/" + "Premio1.png")
            screen.blit(backGround,(0,0))
            screen.blit(premio,(0,0))
            placarGeral = open("placar.txt","r") #abre o placar (no cliente, sincronizar com servidor)
            textoL = placarGeral.read().splitlines()
            placarGeral.close()
            placarGeral = open("placar.txt","w")
            existente = False
            if f[1] % 2 != contTurno % 2: #Verifica quem ganhou
                vencedor = Jog1
            else:
                vencedor = Jog2
            vencedor.Pontuação += recompensa #Aumenta a pontuação, e mostra o vencedor
            ImprimirVisual(["Vencedor", "********", "{}!".format(vencedor.Nome)], alturaInicial=480,
                            posiçãoInicial=530, espaço=20, cor=(0, 0, 255))
            searchPatter = re.compile("^" + str(vencedor.Nome) + ".*[0-9]$") #Procura se o nome já existe com regex
            for i in range(len(textoL)): #Incrementa e/ou coloca a pontuação daquele nome
                if re.match(searchPatter, textoL[i]):
                    existente = True
                    textoL[i] = searchPatter.sub(str(vencedor.Nome) + " - " + str(vencedor.Pontuação), textoL[i])
            if not existente:
                textoL.append(str(vencedor.Nome) + " - " + str(vencedor.Pontuação))
            del n #Deleta a instância da conexão    
            textoL = "\n".join(textoL)    
            placarGeral.write(textoL)
            placarGeral.close()

        else: #Bom... deu velha
            ImprimirVisual(["Empate <-> Deu velha"], alturaInicial = 750, posiçãoInicial = 470,cor = (0,0,0))
            #Colocar a véinha

        pg.display.flip() 
        pg.time.delay(4000)

        del tabuleiro   #Deleta as instâncias dos jogadores, tabuleiro 
        Jog1, Jog2 = None, None
        tabuleiro = Tabuleiro() #Cria um nome tabuleiro e posições para jogadas
        for i in range(9):
            colliders[i] = pg.Rect(slots[i],(85,95))
        contTurno = 0
        pronto,  jogando, Preparado = False, False, False
        
    pg.display.flip()
    enter = False

#A fazer NESTA VERSÃO:
#Fazer um placar apenas para o multiplayer"online", ideia: Usar Flask ou django
#Coloca os nomes do jogadores jogando (feito, mas só do segundo turno em diante)
#Arruma o sistema de criação pra funcionar com servidor (feito, mas kinda mau feito)
#Resetar os parametros para funcionar mais de 1 jogo (feito, mas kinda mau feito)
#Apenas começar o jogo, quando 2 jogadores estiverem conectados (feito, mas kinda mau feito)

