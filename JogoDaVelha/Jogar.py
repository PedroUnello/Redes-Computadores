import pygame as pg
import re
import random
import sys
from network import Network

def IA(m,lado,alea):
    loopAnterior,jogada = [-1,-1], [-1,-1]
    contador,controle = 0, 0
    indicePleno = [[0,1,2],[3,4,5],[6,7,8]]
    for i in range(len(m)):
        for l in range(len(m[i])):
            if m[i][l] == lado:
                contador +=1
    for j in range(contador):
        for i in range(len(m)):
            for l in range(len(m[i])):
                if m[i][l] == lado and controle < 1 and (i != loopAnterior[0] or l != loopAnterior[1]):   
                    copoI = [i,l]
                    controle += 1
                if m[i][l] == lado:
                    if copoI[0] != i or copoI[1] != l:

                        if copoI[1] == copoI[0] and i == l:
                            if copoI[0] == 0 and i == 1 or copoI[0] == 1 and i == 0:
                                jogada = [2,2]
                            elif copoI[0] == 1 and i == 2 or copoI[0] == 2 and i == 1:
                                jogada = [0,0]
                            elif copoI[0] == 0 and i == 2 or copoI[0] == 2 and i == 0:
                                jogada = [1,1]     

                        elif copoI[1] != l and copoI[0] != i:
                            if ((copoI[0] == 0 and copoI[1] == 2) and (l == 0 and i == 2)) or ((copoI[0] == 2 and copoI[1] == 0) and (i == 0 and l == 2)):
                                jogada = [1,1]
                            elif ((copoI[0] == 0 and copoI[1] == 2) and (l == 1 and i == 1)) or ((copoI[0] == 1 and copoI[1] == 1) and (i == 0 and l == 2)):
                                jogada = [2,0]
                            elif ((copoI[0] == 2 and copoI[1] == 0) and (l == 1 and i == 1)) or ((copoI[0] == 1 and copoI[1] == 1) and (i == 2 and l == 0)):
                                jogada = [0,2]
                            
                        elif copoI[1] == l and copoI[0] != i:

                            if i == 1 and copoI[0] == 0 or copoI[0] == 1 and i == 0:
                                jogada = [2,l]
                            elif i == 0 and copoI[0] == 2 or i == 2 and copoI[0] == 0:
                                jogada = [1,l]
                            elif i == 1 and copoI[0] == 2 or i == 2 and copoI[0] == 1:
                                jogada = [0,l]
                                        
                        elif copoI[0] == i and copoI[1] != l:

                            if l == 1 and copoI[1] == 0 or copoI[1] == 1 and l == 0:
                                jogada = [i,2]
                            elif l == 0 and copoI[1] == 2 or l == 2 and copoI[1] == 0:
                                jogada = [i,1]
                            elif l == 1 and copoI[1] == 2 or l == 2 and copoI[1] == 1:
                                jogada = [i,0]
                                
                    if jogada[0] == -1 and jogada[1] == -1:
                        pass
                    else:
                        if m[jogada[0]][jogada[1]] == 0:
                            return indicePleno[jogada[0]][jogada[1]]
                        
        controle = 0
        loopAnterior = copoI

    while alea:
        jogada = [random.randint(0,2),random.randint(0,2)]
        if m[jogada[0]][jogada[1]] != lado and m[jogada[0]][jogada[1]] == 0:
            return indicePleno[jogada[0]][jogada[1]]
        
    if lado == "X":
        retorno = IA(m,"O",True)
    else:
        retorno = IA(m,"X",True)

    return retorno

def read_pos(str):
    str = str.split(",")
    return [(int(str[0]), int(str[1])),int(str[2]),int(str[3]),str[4]]


def make_pos(tup):
    return str(tup[0][0]) + "," + str(tup[0][1]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])

def CompararPosição(Mouse, Posição, Tamanho):
    if Mouse[1] >= Posição[1] and Mouse[1] <= Posição[1] + Tamanho[1]:
        if Mouse[0] >= Posição[0] and Mouse[0] <= Posição[0] + Tamanho[0]:
            return True
    return False

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

def Checar(matriz):
    contDiagP, contDiagS = ["","",""],["","",""]
    
    for i in range(len(matriz)):
        contLin,contCol = ["","",""],["","",""]

        if matriz[i][i] == "X":
            contDiagP[i] = "X"
        elif matriz[i][i] == "O":
            contDiagP[i] = "O"

        if matriz[i][2-i] == "X":
            contDiagS[i] = "X"
        elif matriz[i][2-i] == "O":
            contDiagS[i] = "O"
        
        for j in range(len(matriz[i])):
            if matriz[i][j] == "X":
                contLin[j] = "X"
            elif matriz[i][j] == "O":
                contLin[j] = "O"
            if matriz[j][i] == "X":
                contCol[j] = "X"
            elif matriz[j][i] == "O":
                contCol[j] = "O"
                
        if contLin == ["X","X","X"] or contCol == ["X","X","X"] or contDiagS == ["X","X","X"] or contDiagP == ["X","X","X"]:
            return True, "X"
        if contLin == ["O","O","O"] or contCol == ["O","O","O"] or contDiagS == ["O","O","O"] or contDiagP == ["O","O","O"]:
            return True, "O"
    
    return False, None

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
                    #printar tabuleiro
                    #screen.blit(mao,(colliders[i][0]+10,colliders[i][1]-10))
                    #printar mão no ponto da jogada, no tabuleiro
                    #reprintar tabuleiro
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
    Imagem = ''
    ganhador,finalizado = False, False
    
    matriz = [[0,0,0],[0,0,0],[0,0,0]]

    def CriarPontos(self,lado,pos):
        if lado != None:
            self.matriz[pos[0]][pos[1]] = lado

    def Status(self):
        if Checar(self.matriz)[0]:
            self.finalizado = True
            if Checar(self.matriz)[1] != None:
                self.ganhador = Checar(self.matriz)[1]


pg.init()
largura = 1000
altura = 1000
screen = pg.display.set_mode((largura, altura))
pg.display.set_caption("Jogo da Velha WIP")
screen.fill((0,0,0))
pg.display.flip()

jogar, enter, criando, jogandoM, jogandoS, jogando, desenhando = True, False, False, False, False, False, False
lado,userInput = ["X","O"], ['']
contTurno = 0
pos = (0,0)
slots = [(400,430),(500,430),(600,430),(400,520),(500,520),(600,520),(400,610),(500,610),(600,610)]
colliders = [0] * 9
tabuleiro = Tabuleiro()
tabuleiro.matriz = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
tabuleiro.Imagem = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Tabu1.png")
for i in range(9):
    colliders[i] = pg.Rect(slots[i], (85, 95))
Jog2, Jog1 = None, None
while True:

    while jogar:
        
        for event in pg.event.get():

            if event.type == pg.MOUSEBUTTONDOWN:
                if jogando:
                    if jogandoM:
                        if f[1]%2 == contTurno%2:
                            if pg.mouse.get_pressed()[0]:
                                pos = pg.mouse.get_pos()
                                print(pos)
                        else:
                            pass
                    else:
                        if pg.mouse.get_pressed()[0]:
                            pos = pg.mouse.get_pos()
                            print(pos)
                else:
                    if pg.mouse.get_pressed()[0] and not (CompararPosição(pos, BotãoMulti.Posição, (90,30)) or CompararPosição(pos, BotãoSingle.Posição, (90,30))):
                        pos = pg.mouse.get_pos()
                        print(pos)


            if event.type == pg.KEYDOWN:
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

        if not jogando:
            if not desenhando:
                pg.time.delay(2000)
                screen.blit(tabuleiro.Imagem,(0,0))
                desenhando = True
            barraCriacao = pg.Rect(50,50,90,30)
            corA = (0,255,0)
            BotãoSingle = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão2.png"),(385,300),["Single"],"PlaceHolder")
            BotãoMulti = Botão(pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Botão4.png"),(610,300),["Multi"],"PlaceHolder")
            screen.blit(BotãoSingle.Imagem,BotãoSingle.Posição)
            screen.blit(BotãoMulti.Imagem,BotãoMulti.Posição)
            ImprimirVisual(BotãoMulti.Nome,None,None,BotãoMulti.Posição[1]+15,BotãoMulti.Posição[0]+40)
            ImprimirVisual(BotãoSingle.Nome,None,None,BotãoSingle.Posição[1]+16,BotãoSingle.Posição[0]+25)

        if criando and not enter:
            text = font.render(userInput[0], True, corA)
            tLargura = max(200,text.get_width() +10)
            barraCriacao.w = tLargura
            pg.draw.rect(screen,(0,0,0),barraCriacao)
            screen.blit(text, (barraCriacao.x+5, barraCriacao.y+5))
            pg.draw.rect(screen, corA, barraCriacao, 2)

        if criando and enter:
            userInput[0] = userInput[0].lower()
            userInput[0] = userInput[0][0].upper() + userInput[0][1:]
            pg.draw.rect(screen,(0,0,0),(50,50,90,30))#Remover
            if Jog1 == None:
                Jog1 = Jogador(userInput[0],0,["X","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/X1.png"])
            elif Jog2 == None:
                Jog2 = Jogador(userInput[0],0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
            userInput = ['']
            criando = False
            
        listaJogadores = [Jog1,Jog2]
        
        if CompararPosição(pos, BotãoMulti.Posição, BotãoMulti.Imagem.get_rect().size) or CompararPosição(pos, BotãoSingle.Posição, BotãoSingle.Imagem.get_rect().size) and not jogando:
            
            if CompararPosição(pos, BotãoMulti.Posição, BotãoMulti.Imagem.get_rect().size):#Trocar por image.get_rect().size
                if Jog1 == None:
                    font = pg.font.Font(None, 32)
                    criando = True
                else:
                    n = Network()
                    f = read_pos(n.getPos())
                    #f[2] = 1
                    #f[3] = Jog1.Nome
                    Jog2 = Jogador("",0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
                    jogandoM = True
                    recompensa = 20
                pg.display.flip()
   
            if CompararPosição(pos, BotãoSingle.Posição, BotãoSingle.Imagem.get_rect().size):#Trocar por image.get_rect().size
                if Jog1 == None:
                    font = pg.font.Font(None,32)
                    criando = True
                else:
                    if random.randint(1,2) == 1:
                        Jog2 = Jog1
                        Jog1 = Jogador("Bot134679",0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
                    else:
                        Jog2 = Jogador("Bot134679",0,["O","/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/O1.png"])
                    #Como não tem opção para escolha de lado
                    jogandoS = True
                    recompensa = 10
                pg.display.flip()
                #Dificuldade

            if jogandoS or jogandoM:    
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
            pg.draw.line(screen,(100,0,0),(460,300),(500,340),3)
            pg.draw.line(screen,(100,0,0),(500,300),(460,340),3)
            pg.draw.circle(screen,(0,0,100),(650,310),20,3)
            if Jog1.Nome == "Bot134679":
                if lado[contTurno%2] == "O":
                    pg.draw.line(screen,(255,0,0),(460,300),(500,340),3)
                    pg.draw.line(screen,(255,0,0),(500,300),(460,340),3)
                elif lado[contTurno%2] == "X":
                    pg.draw.circle(screen,(0,0,255),(650,310),20,3)
            else:
                if lado[contTurno%2] == "X":
                    pg.draw.line(screen,(255,0,0),(460,300),(500,340),3)
                    pg.draw.line(screen,(255,0,0),(500,300),(460,340),3)
                elif lado[contTurno%2] == "O":
                    pg.draw.circle(screen,(0,0,255),(650,310),20,3)
            
            if jogandoS:
                jogadorAtual = listaJogadores[contTurno%2]
                if jogadorAtual.Nome == "Bot134679":
                    jogadaBot = IA(tabuleiro.matriz,jogadorAtual.Lado[0],False)
                    if jogadaBot != None:
                        pos = (slots[jogadaBot][0] + 50,slots[jogadaBot][1] +50)
                        jogadaBot = None
                jogadorAtual.Jogar(pos,colliders)
                if jogadorAtual.valido:
                    contTurno +=1
                    jogadorAtual.valido = False
                    jogadorAtual = None
                    pos = (0,0)
                    tabuleiro.Status()
                    pg.display.flip()
                    
            if jogandoM:
                hold = read_pos(n.send(make_pos([pos,contTurno,1,Jog1.Nome])))
                if hold[2] != 0:
                    Jog2.Nome = hold[3]
                    for i in range(len(textoL)):
                        if re.match("\A" + str(Jog2.Nome), textoL[i]):
                            Jog2.Pontuação = int(re.findall(".[0-9][0-9]$",textoL[i])[0])
                    jogadorAtual = listaJogadores[hold[1]%2]
                    jogadorAtual.Jogar(hold[0],colliders)
                    jogadorAtual = listaJogadores[contTurno%2]
                    jogadorAtual.Jogar(pos,colliders)
                    if jogadorAtual.valido:
                        if f[1] % 2 == 0:
                            ImprimirVisual([Jog1.Nome], alturaInicial=265, posiçãoInicial=450, cor=(0, 0, 0))
                            ImprimirVisual([Jog2.Nome], alturaInicial=265, posiçãoInicial=620, cor=(0, 0, 0))
                        else:
                            ImprimirVisual([Jog2.Nome], alturaInicial=265, posiçãoInicial=450, cor=(0, 0, 0))
                            ImprimirVisual([Jog1.Nome], alturaInicial=265, posiçãoInicial=620, cor=(0, 0, 0))
                        contTurno +=1
                        jogadorAtual.valido = False
                        jogadorAtual = None
                        pos = (0,0)
                        tabuleiro.Status()
                        pg.display.flip()
                
        if tabuleiro.finalizado or contTurno == 9:            
            if tabuleiro.finalizado:
                pg.time.delay(2000)
                screen.fill((0,0,0))
                backGround = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/BackGround.jpeg")
                premio = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Premio1.png")
                screen.blit(backGround,(0,0))
                screen.blit(premio,(0,0))
                placarGeral = open("placar.txt","r")
                texto = placarGeral.read()
                textoL = texto.splitlines()
                placarGeral.close()
                placarGeral = open("placar.txt","w")

                if Jog2.Nome != "Bot134679" and Jog1.Nome != "Bot134679":
                    if f[1] % 2 != contTurno % 2:
                        existente = False
                        Jog1.Pontuação += recompensa
                        ImprimirVisual(["Vencedor", "********", "{}!".format(Jog1.Nome)], alturaInicial=480,
                                       posiçãoInicial=530, espaço=20, cor=(255, 0, 0))
                        searchPatter = re.compile("^" + str(Jog1.Nome) + ".*[0-9]$")

                        for i in range(len(textoL)):
                            if re.match(searchPatter, textoL[i]):
                                existente = True
                                textoL[i] = searchPatter.sub(str(Jog1.Nome) + " - " + str(Jog1.Pontuação), textoL[i])
                        if not existente:
                            textoL.append(str(Jog1.Nome) + " - " + str(Jog1.Pontuação))
                        del n

                    else:
                        existente = False
                        Jog2.Pontuação += recompensa
                        ImprimirVisual(["Vencedor", "********", "{}!".format(Jog2.Nome)], alturaInicial=480,
                                       posiçãoInicial=530, espaço=20, cor=(0, 0, 255))
                        searchPatter = re.compile("^" + str(Jog2.Nome) + ".*[0-9]$")

                        for i in range(len(textoL)):
                            if re.match(searchPatter, textoL[i]):
                                existente = True
                                textoL[i] = searchPatter.sub(str(Jog2.Nome) + " - " + str(Jog2.Pontuação), textoL[i])
                        if not existente:
                            textoL.append(str(Jog2.Nome) + " - " + str(Jog2.Pontuação))
                        del n
                else:
                    if contTurno%2 == 0 and Jog2.Nome != "Bot134679":
                        existente = False
                        Jog2.Pontuação += recompensa
                        ImprimirVisual(["Vencedor","********","{}!".format(Jog2.Nome)],alturaInicial = 480, posiçãoInicial = 530,espaço = 20, cor = (0,0,255))
                        searchPatter = re.compile("^" + str(Jog2.Nome) + ".*[0-9]$")

                        for i in range(len(textoL)):
                            if re.match(searchPatter, textoL[i]):
                                existente = True
                                textoL[i] = searchPatter.sub(str(Jog2.Nome) + " - " + str(Jog2.Pontuação),textoL[i])
                        if not existente:
                            textoL.append(str(Jog2.Nome) + " - " + str(Jog2.Pontuação))

                    elif contTurno%2 == 1 and Jog1.Nome != "Bot134679":
                        existente = False
                        Jog1.Pontuação += recompensa
                        ImprimirVisual(["Vencedor","********","{}!".format(Jog1.Nome)],alturaInicial = 480, posiçãoInicial = 530,espaço = 20, cor = (255,0,0))
                        searchPatter = re.compile("^" + str(Jog1.Nome) + ".*[0-9]$")

                        for i in range(len(textoL)):
                            if re.match(searchPatter, textoL[i]):
                                existente = True
                                textoL[i] = searchPatter.sub(str(Jog1.Nome) + " - " + str(Jog1.Pontuação),textoL[i])
                        if not existente:
                            textoL.append(str(Jog1.Nome) + " - " + str(Jog1.Pontuação))

                    else:
                        ImprimirVisual(["Vencedor","********","Máquina!"],alturaInicial = 480, posiçãoInicial = 530, cor = (0,255,0))
                    
                texto = "\n"
                texto = texto.join(textoL)    
                placarGeral.write(texto)
                placarGeral.close()
                pg.display.flip() 

            else:
                ImprimirVisual(["Empate <-> Deu velha"], alturaInicial = 750, posiçãoInicial = 470,cor = (0,0,0))
                pg.display.flip()
                
            pg.time.delay(4000)
            del tabuleiro
            tabuleiro = Tabuleiro()
            tabuleiro.matriz = [[0,0,0],[0,0,0],[0,0,0]]
            tabuleiro.Imagem = pg.image.load("/home/pedrou/Documentos/VSCodeWS/JogoDaVelha/img/Tabu1.png")
            for i in range(9):
                colliders[i] = pg.Rect(slots[i],(85,95))
            Jog2,Jog1 = None, None
            contTurno = 0
            jogandoM, jogandoS, jogando, Preparado, jogar, desenhando = False, False, False, False, True, False
            
        pg.display.flip()
        enter = False

#A fazer NESTA VERSÃO:
#Fazer um placar apenas para o multiplayer"online", ideia: Usar Flask ou django
#Coloca os nomes do jogadores jogando (feito, mas só do segundo turno em diante)
#Arruma o sistema de criação pra funcionar com servidor (feito, mas kinda mau feito)
#Resetar os parametros para funcionar mais de 1 jogo (feito, mas kinda mau feito)
#Apenas começar o jogo, quando 2 jogadores estiverem conectados (feito, mas kinda mau feito)

