import pygame
import math
from random import randint
from collections import defaultdict
from pygame import mixer
import io

#Pasar a bytes la fuente
def to_bytes(font):
    with open(font, 'rb') as f:
        ttf_to_bytes=f.read()
    return io.BytesIO(ttf_to_bytes)
fuente_general=to_bytes("./fonts/fuente.ttf")
#inicializar pygame
pygame.init()
#pantalla
dsp=pygame.display.set_mode((800,700))
#fondo
fondo_img=pygame.image.load("./assets/fondo.jpg")
#titulo
pygame.display.set_caption("Space Wars")
icono=pygame.image.load("./assets/meteor.png")
pygame.display.set_icon(icono)
#player

player_img=pygame.image.load("./assets/player.png")
px=368
py=600
def jugador(X,Y):
    dsp.blit(player_img,(X,Y))

##Enemies 

def enemigo(img,x,y):
    dsp.blit(img,(x,y))

#generar varios enemigos de manera poco eficiente

enemy_img=defaultdict()
ex=defaultdict()
ey=defaultdict()
factorx=defaultdict(float)
factory=defaultdict(float)
estadia=defaultdict(int) #el estado de la explosion
cant_enemies=8
for e in range(cant_enemies):
    enemy_img[e]=pygame.image.load("./assets/enemy.png")
    ex[e]=randint(0,736)
    ey[e]=randint(50,200)
    factorx[e]=randint(1,3)/10
    factory[e]=0.05
    estadia[e]=700

#balas
shot_img=pygame.image.load("./assets/shot.png")
shot_speed=1
visible=False
by=580
bx=0

def shoot(x,y):
    global visible
    visible=True
    dsp.blit(shot_img,(x,y))


#colisiones y explosiones

explosiones=[]

for i in range(cant_enemies):
    tmp = defaultdict()
    tmp["ex1"]=pygame.image.load("./assets/explosion.png")
    tmp["ex2"]=pygame.image.load("./assets/explosion2.png")
    tmp["ex3"]=pygame.image.load("./assets/explosion3.png")
    tmp["visible"]=False
    tmp["x"]=0
    tmp["y"]=0
    explosiones.append(tmp)


def explosion(i1,i2,i3,x,y,estadia):
    if estadia>500:
        dsp.blit(i1,(x,y))
    elif estadia >250:
        dsp.blit(i2,(x,y))
    else:
        dsp.blit(i3,(x,y))

def colision(x1,y1,x2,y2):
    impacto=math.sqrt(math.pow(x2-x1,2) + math.pow(y2-y1,2))
    if impacto>27:
        return False
    else:
        
        return True





#Puntaje
puntaje=0
texto=pygame.font.Font(fuente_general,32)
def mostrar_puntaje():
    txt=f"Puntaje:  {puntaje}"
    string=texto.render(txt,True,(255,255,255),(0,0,0))
    dsp.blit(string,(10,10)) # el string se maneja como imagen
#SONIDO DE FONDO
mixer.music.load("./sounds/music.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.1)
#SONIDOS EFECTOS
shoot_sound=mixer.Sound("./sounds/shoot.ogg")
colision_sound=mixer.Sound("./sounds/destroy.ogg")

#Game Over

def game_over():
    fuente=pygame.font.Font(to_bytes("./fonts/fuente.ttf"),40)
    texto=fuente.render("Game Over",True,(255,255,255),(0,0,0))
    dsp.blit(texto,(268,300))

#Ejecución
runn =True


while runn:
    #pintar fondo de pantalla
    #se lo ubica primero para que por cada iteración no tape lo demas..
    #dsp.fill((24, 9, 70 ))
    dsp.blit(fondo_img,(0,0))
    
    keys=pygame.key.get_pressed()
    
    
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            runn=False
    
    if keys[pygame.K_s]:
        if px>0:
            px-=0.5
    if keys[pygame.K_f]:
        if px<736:
            px+=0.5

    if keys[pygame.K_SPACE]:
        
        if not visible:
            shoot_sound.play()
            bx=px
            shoot(bx+28,py+1)
       
    
    if by==0:
        visible=False
        by=600

    if visible:
        by-=shot_speed
        shoot(bx+28,by+1)

    for indice in range(cant_enemies):
           

            ex[indice]+=factorx[indice]
            if ex[indice]>736:
                factorx[indice]= -factorx[indice]
            if ex[indice]<0:
                factorx[indice]= -factorx[indice]
            ey[indice]+=factory[indice]

    

   
    #print jugador    
    jugador(px,py)
    #print enemigo
    for i in range(cant_enemies):
        #enemigo colisiona con el jugador
        if colision(ex[i],ey[i],px,py) or ey[i]>=py:
            for k in range(cant_enemies):
                ey[k]=1000
                game_over()
            
            break
        #la bala lo ataca
        elif colision(ex[i],ey[i],bx,by):
            
            colision_sound.play()
            explosiones[i]["visible"]=True
            explosiones[i]['x']=ex[i]
            explosiones[i]['y']=ey[i]
            visible=False
            by=580
            ex[i]=randint(0,736)
            ey[i]=randint(50,200)
            puntaje+=1

        #enemigo antes asi no se superpone a la explosion
        enemigo(enemy_img[i],ex[i],ey[i])
        
        if explosiones[i]["visible"]:
            estadia[i]-=1
            if estadia[i]<1:
                estadia[i]=700
                explosiones[i]["visible"]=False
            
            explosion(explosiones[i]['ex1'],explosiones[i]['ex2'],explosiones[i]['ex3'],explosiones[i]['x'],explosiones[i]['y'],estadia[i])
        
    #mostramos el puntaje
    mostrar_puntaje()    
    #final de cada iteración donde se refresca y se actualiza la pantalla..
    pygame.display.update()

