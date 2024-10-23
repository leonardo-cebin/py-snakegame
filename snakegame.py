from tkinter import *
import time
import random
from PIL import Image

lighterColor = '#648011'  #code of the lighter color, to be used on game screen
darkerColor = '#42540B'    #code of the darker color, to be used on game score
blueColor = '#0000FF'

bite = False

grid_width = 40   #FUNCIONA!!!
grid_height = 35
snakeDefault = [[15, 10, 11]]      #posição inicial da cobra
snake = [[15, 10, 11]]
default_size = 20         #tamanho inicial da cobra
grade = [[None]*grid_height for i in range(grid_width)]   #List comprehension         #ESTUDAR MAIS ISSO
state = 3       #Clockwise
speed = 0.08   #less is faster, more is slower
running = BooleanVar
prizeX = IntVar
prizeY = IntVar
score = 0
lastState = None
sprize = False


#states: 0 to head, 1 to left, 2 to up, 3 to SW, 4 to NE, 5 to NW, 6 to SE, 7 to belly, 8 to tail, 11 to right, 12 to down


def gridFormation():
    global grade
    for i in range(grid_width):  # I será sempre o X
        for j in range(3, grid_height):  # J será sempre o Y
            # Label(janela,text='X:{0} Y:{1}'.format(i,j),bd=2,relief=RIDGE,width=1,height=1,padx=10,pady=10).grid(row=j,column=i)  debug with coordinates
            grade[i][j] = Label(janela, image=pixel, bg=lighterColor)
            grade[i][j].grid(row=j, column=i)
    janela.update()

def telarefresh():
    global grade
    for i in range(grid_width):  # I será sempre o X
        for j in range(3, grid_height):  # J será sempre o Y
            # Label(janela,text='X:{0} Y:{1}'.format(i,j),bd=2,relief=RIDGE,width=1,height=1,padx=10,pady=10).grid(row=j,column=i)  debug with coordinates
            grade[i][j] = Label(janela, image=pixel, bg=lighterColor)

def starter():
    global state, score, snake, speed, default_size
    if running == True: return 0
    state = 3
    speed = 1 / int(spinBoxSpeed.get())
    default_size = int(spinBoxLength.get())
    score = 0
    scored.config(text=score)
    feeder()

    #telarefresh()

    snakeCenterize()
    rodando()

def snakeCenterize():
    global snake, grade, snakeDefault
    snake = []
    snake = [[15, 10, 11]]
    for i in range(1, default_size):
        snake.append([snake[i - 1][0] - 1, snake[i - 1][1], 11])

def rodando():
    global bite
    global running
    running = True

    while running:
        stateChange()
        if bite == True:
            bite = False
            return 0
        janela.update()
        time.sleep(speed)


def feeder():
    global grade, prizeX, prizeY, sprize
    if sprize: sprize = False
    grade[prizeX := random.randrange(0, grid_width)][prizeY := random.randrange(3, grid_height)].config(image=frog)

    if random.randrange(0,32) == 7:
        grade[prizeX][prizeY].config(image=star)
        sprize = True
        #janela.after(10000, feeder)

    return prizeX, prizeY

def stateChange():
    global running,score,lastState,sprize, lighterColor, blueColor, bite, head

    if not running: return 0

    snakeLastBit = snake[len(snake) - 1][2]
    try:
        if state == 1:     #LEFT
            if snake[0][2] == 2:
                snake.insert(0, [snake[0][0] - 1, snake[0][1], 4])
            elif snake[0][2] == 12:
                snake.insert(0, [snake[0][0] - 1, snake[0][1], 6])
            else:
                snake.insert(0, [snake[0][0] - 1, snake[0][1], 1])
        if state == 2:     #UP
            if snake[0][2] == 1:
                snake.insert(0, [snake[0][0], snake[0][1] - 1, 3])
            elif snake[0][2] == 11:
                snake.insert(0, [snake[0][0], snake[0][1] - 1, 6])
            else:
                snake.insert(0, [snake[0][0], snake[0][1] - 1, 2])
        if state == 3:     #RIGHT
            if snake[0][2] == 12:
                snake.insert(0, [snake[0][0] + 1, snake[0][1], 3])
            elif snake[0][2] == 2:
                snake.insert(0, [snake[0][0] + 1, snake[0][1], 5])
            else:
                snake.insert(0, [snake[0][0] + 1, snake[0][1], 11])
        if state == 4:     #DOWN
            if snake[0][2] == 1:
                snake.insert(0, [snake[0][0], snake[0][1] + 1, 5])
            elif snake[0][2] == 11:
                snake.insert(0, [snake[0][0], snake[0][1] + 1, 4])
            else:
                snake.insert(0, [snake[0][0], snake[0][1] + 1, 12])
    except IndexError:
        running = False
        return 0
# states: 0 to head, 1 to left, 2 to up, 3 to SW, 4 to NE, 5 to NW, 6 to SE, 7 to belly, 8 to tail, 11 to right, 12 to down
    if snake[0][0] < 0 or snake[0][1] < 0:     #impede problema da tela lib left
        running = False
        return 0

        # Condição de derrota, tail bite
    for v in range(1, len(snake) - 1):
         if snake[0][0] == snake[v][0] and snake[0][1] == snake[v][1]:
            running = False
            bite = True
            return 0

    grade[snake[0][0]][snake[0][1]].config(bg=lighterColor, image=head[state-1])   #código da cabeça

    try:
        if snake[0][1] == 2:     #Verifica se ela saiu do screen e para o game
            running = False
            return 0

        tailBit = grade[snake[len(snake) - 1][0]][snake[len(snake) - 1][1]]

        if snake[1][2] == 4:
            grade[snake[2][0]][snake[2][1]].config(bg=lighterColor, image=cornerNE)
        elif snake[1][2] == 6:
            grade[snake[2][0]][snake[2][1]].config(bg=lighterColor, image=cornerSE)
        elif snake[1][2] == 5:
            grade[snake[2][0]][snake[2][1]].config(bg=lighterColor, image=cornerNW)
        elif snake[1][2] == 3:
            grade[snake[2][0]][snake[2][1]].config(bg=lighterColor, image=cornerSW)

        if (snake[1][2] == 1 or snake[1][2] == 11): grade[snake[1][0]][snake[1][1]].config(bg=lighterColor, image=bodyH)
        if (snake[1][2] == 2 or snake[1][2] == 12): grade[snake[1][0]][snake[1][1]].config(bg=lighterColor, image=bodyV)

        for u in range(1,len(snake)-1):
            if snake[u][2] == 3 or snake[u][2] == 4 or snake[u][2] == 5 or snake[u][2] == 6:
                if snake[u-1][2] == 1 or snake[u-1][2] == 11:
                    grade[snake[u][0]][snake[u][1]].config(bg=lighterColor, image=bodyH)
                elif snake[u-1][2] == 2 or snake[u-1][2] == 12:
                    grade[snake[u][0]][snake[u][1]].config(bg=lighterColor, image=bodyV)

        if snake[1][2] == 7: grade[snake[1][0]][snake[1][1]].config(image=bellyH)
        if snake[1][2] == 17: grade[snake[1][0]][snake[1][1]].config(image=bellyV)

        #FUNCIONANDO
        tailBit.config(bg=lighterColor, image=pixel)    #isto aqui é para o espaço após a cauda voltar ao original
        if not(lastState):     #Será usado apenas no primeiro frame, para evitar bugs
            lastState = tailBit
        lastState.config(bg=lighterColor, image=pixel)
        lastState = tailBit

        #Tail orientation FUNCIONANDO
        if snake[len(snake) - 1][2] == 1:
            tailBit.config(bg=lighterColor, image=tailL)
        if snake[len(snake) - 1][2] == 11:
            tailBit.config(bg=lighterColor, image=tailR)
        if snake[len(snake) - 1][2] == 2:
            tailBit.config(bg=lighterColor, image=tailU)
        if snake[len(snake) - 1][2] == 12:
            tailBit.config(bg=lighterColor, image=tailD)

        if not (snake[0][0] == prizeX and snake[0][1] == prizeY):
            del snake[-1]
        else:
            if not sprize:
                score += 1
            else:
                score += 10

            #scored.set(score)
            scored.config(text=score)

            #if score > 30:
            #    lighterColor = blueColor

            if snake[0][2] == 1 or snake[0][2] == 11: snake[0][2] = 7
            if snake[0][2] == 2 or snake[0][2] == 12: snake[0][2] = 17
            #belly codea

            feeder()

            for i in snake:
                if i[0] == prizeX and i[1] == prizeY:
                   feeder()
                   break

    except IndexError:
        running = False


def keyA(event):
    global state
    if state == 1 or state == 3:
        return 0
    elif state == 2 or state == 4:
        state = 1
    stateChange()
def keyW(event):
    global state
    if state == 2 or state == 4:
        return 0
    elif state == 1 or state == 3:
        state = 2
    stateChange()
def keyS(event):
    global state
    if state == 2 or state == 4:
        return 0
    elif state == 1 or state == 3:
        state = 4
    stateChange()
def keyD(event):
    global state
    if state == 1 or state == 3:
        return 0
    elif state == 2 or state == 4:
        state = 3
    stateChange()

janela = Tk()
janela.title('Jogo da Cobrinha - Meu nostálgico projeto de Python')
janela.iconbitmap('assets/python.ico')

pixel = PhotoImage(file='assets/pixel.png')
pixelSnake = PhotoImage(file='assets/pixelSnake.png')
pixelScreen = PhotoImage(file='assets/screen.png')
frog = PhotoImage(file='assets/food.png')
bodyH = PhotoImage(file='assets/body-segment-horizontal.png')
bodyV = PhotoImage(file='assets/body-segment-vertical.png')
tailL = PhotoImage(file='assets/tail-segment-0.png')
tailU = PhotoImage(file='assets/tail-segment-1.png')
tailR = PhotoImage(file='assets/tail-segment-11.png')
tailD = PhotoImage(file='assets/tail-segment-12.png')
cornerSW = PhotoImage(file='assets/corner-SW.png')
cornerNW = PhotoImage(file='assets/corner-NW.png')
cornerNE = PhotoImage(file='assets/corner-NE.png')
cornerSE = PhotoImage(file='assets/corner-SE.png')

head = []
for z in range (1,5): head.append(PhotoImage(file='assets/head-{0}.png'.format(z)))

bellyV = PhotoImage(file='assets/body-segment-bellyH.png')
bellyH = PhotoImage(file='assets/body-segment-bellyV.png')
star = PhotoImage(file='assets/star.png')
start = PhotoImage(file='assets/start.png')
start = start.subsample(2,2)
credits = PhotoImage(file='assets/name.png')
phone = PhotoImage(file='assets/phone.png')



gridFormation()
snakeCenterize()    #MELHOR NÃO MEXER

#grade[snake[i][0]][snake[i][1]].config(bg='black',image=pixelSnake)
#grade[snake[0][0]][snake[0][1]].config(bg='black',image=pixelSnake)

for i in range(grid_width):   # I será sempre o X
    for j in range(3):    # J será sempre o Y
        #Label(janela,text='X:{0} Y:{1}'.format(i,j),bd=2,relief=RIDGE,width=1,height=1,padx=10,pady=10).grid(row=j,column=i)  debug with coordinates
        grade[i][j] = Label(janela, image=pixelScreen,bg=darkerColor,padx=0,pady=0)
        grade[i][j].grid(row=j,column=i)

scored = Label(janela,text='{0}'.format(score),font=('System',34),bg=darkerColor)
scored.grid(row=0, column=1, columnspan=3, rowspan=3)
creditos = Label(janela,image=credits,bg=darkerColor,underline=True)
creditos.grid(row=0,column=24,columnspan=18,rowspan=2)

botao = Button(janela,image=start,bg=darkerColor,command=starter)
botao.grid(row=0,column=14,columnspan=10,rowspan=3)

labelSpeed = Label(janela,text="Speed: ", font=('System',9),bg=darkerColor,padx=0,pady=0)
labelLength = Label(janela,text="Length: ", font=('System',9),bg=darkerColor,padx=0,pady=0)
spinBoxSpeed = Spinbox(janela,from_=5,to=30,wrap=False,width=3,bg=darkerColor)
spinBoxLength = Spinbox(janela,from_=3,to=20,wrap=True,width=3,bg=darkerColor)

spinBoxSpeed.grid(row=0,column=10,columnspan=2)
spinBoxLength.grid(row=1,column=10,columnspan=2)
labelSpeed.grid(row=0,column=7,columnspan=3)
labelLength.grid(row=1,column=7,columnspan=3)


janela.bind('<a>', keyA)
janela.bind('<w>', keyW)
janela.bind('<d>', keyD)
janela.bind('<s>', keyS)
janela.bind('<Escape>', quit)


#xx = janela.winfo_screenwidth()
#yy = janela.winfo_screenheight()
#janela.geometry('{}x{}+{}+{}'.format(grid_width*16,grid_height*16,int(xx)-grid_width*16,int(yy)-grid_height*16))

janela.eval('tk::PlaceWindow . center')    #very useful line!!!
janela.resizable(False, False)
janela.update()
janela.mainloop()