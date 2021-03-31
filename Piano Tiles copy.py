import pygame
import random


pygame.mixer.pre_init(48000, -16, 1, 1024)
pygame.init()
pygame.mixer.init()

# for the sound effects

# GLOBAL COLOURS
BLACK=(0,0,0)
WHITE=(255,255,255)
GREY=(169,169,169)
RED=(255,0,0)
GREEN=(0,200,0)

# GLOBAL VARIABLES
sHeight=600
sWidth=400
size=(sWidth, sHeight)
start_speed=3
score=0
tileWidth = 100
tileHeight = 150

screen=pygame.display.set_mode(size)
pygame.display.set_caption("Piano Tiles")
clock=pygame.time.Clock()
FPS=50
tileList=pygame.sprite.Group()
deadTiles=pygame.sprite.Group()
redTiles=pygame.sprite.Group()
HIGHSCORE_FILE='hs.txt'
SOUND_FILE= 'Activate.wav'
JINGLE_BELLS='Piano Songs/Jingle Bells.txt'
MARIO='Piano Songs/Mario FANCY.txt'
S_TRUE = 'Piano Songs/Sincerely True.txt'
activateSound=pygame.mixer.Sound(SOUND_FILE)
                                                                                                                                              
def getHS():
    """Returns the current high score by reding from the high score text file"""
    try:
        with open (HIGHSCORE_FILE,'r') as file:
            hscore = int(file.readline())
        return hscore
    except:
        hscore = 0
        with open(HIGHSCORE_FILE,'w') as file:
            file.write(str(hscore))
        
def newHS(newHigh):
    """Overwrites the current high score in the text file withe a new high score"""
    with open(HIGHSCORE_FILE,'w') as file:
            file.write(str(newHigh))
            
def draw_bg():
    """Draws 3 vertical lines on the game screen"""
##    for x in range(0, sHeight, tileHeight):
##        pygame.draw.line(screen,BLACK,(0,x),(sWidth,x))
    for y in range(0, sWidth, tileWidth):
        pygame.draw.line(screen,BLACK,(y,0),(y,sHeight))
        
class Tile(pygame.sprite.Sprite):
    def __init__(self, colour, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([width,height])
        self.image.fill(colour)
        self.rect=self.image.get_rect()
        self.speed=speed
    def move(self,speed):
        if self.rect.y<550:
            self.rect.y+=self.speed
            return True
        else:    
            return False
    def deadMove(self,speed):
        self.rect.y+=self.speed*2
# initialise the first 4 tiles to start the game
possibleX=[0]
start_y=-2*tileHeight
for i in range(4):
    tile=Tile(BLACK,tileWidth, tileHeight,start_speed)
    xcor=random.choice(possibleX)
    tile.rect.x=xcor
    tile.rect.y=start_y
    tileList.add(tile)
    start_y+=tileHeight
    
def getLowestTile():
    """Returns the instance of tile object which is lowest on the screen """
    tiles=dict()
    tilesY=list()
    for tile in tileList:
        tiles.update({tile.rect.y:tile})
        tilesY.append(tile.rect.y)
    lowestY=max(tilesY)
    return tiles[lowestY]

def getHighestTile():
    """Returns the instance of tile object which is highest on the screen"""
    tilesY=list()
    for tile in tileList:
        tilesY.append(tile.rect.y)
    highestY=min(tilesY)
    return highestY     

def drawTextCent(text, font, fontSize, color, x, y):
    Text=pygame.font.SysFont(font, fontSize)
    textSurface=Text.render(text, True, color)
    textRect=textSurface.get_rect()
    textRect.center=(x,y)
    screen.blit(textSurface,textRect)
    return textRect

def drawText_TopLeft(text, font, fontSize, color, x):
    Text=pygame.font.SysFont(font, fontSize)
    textSurface=Text.render(text, True, color)
    textRect=textSurface.get_rect()
    textRect.bottom=x
    screen.blit(textSurface,textRect)
    return textRect

def show_endScreen():
    global score
    # Display end game texts
    screen.fill(WHITE)
    drawTextCent("GAME OVER", 'arial', 50, RED, sWidth/2,sHeight*0.4)
    drawTextCent("YOUR SCORE: "+ str(score), 'arial', 50, BLACK,sWidth/2,sHeight*0.5)
    drawTextCent("Press the 'n' key to begin a new game", 'arial', 30, BLACK, sWidth/2,sHeight*0.6)
    pygame.display.update()

    # wait for input from user 
    waiting=True
    while waiting:
        for event in pygame.event.get():
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_n:
                    waiting=False
            if event.type==pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    quit()
            elif event.type==pygame.QUIT:
                quit()
                
    # if the while loop is broken, re-initialise the necessaryvariables
    score=0
##    possibleX=[0,tileWidth,2*tileWidth,3*tileWidth]
    possibleX=[0]
    start_y=-2*tileHeight
    tileList.empty()
    deadTiles.empty()
    redTiles.empty()
    for i in range(4):
        tile=Tile(BLACK,tileWidth, tileHeight,start_speed)
        xcor=random.choice(possibleX)
        tile.rect.x=xcor
        tile.rect.y=start_y
        tileList.add(tile)
        start_y+=tileHeight
    
    game_loop()
    
def show_score():
    """Displays the live score on the top left of the screen"""
    global score
    drawText_TopLeft(str(score),'arial',40,GREEN,35)


def show_HS():
    """Displays the high score below the live score"""
    high=getHS()
    drawText_TopLeft("HS: " + str(high),'arial',40,GREEN,65)
    pygame.display.update()
    
def playNote(song, chord, index1, index2=0, index3=0, index4=0):
    """Plays the audio files of up to 3 notes corresponding to that in the list of notes to be played.
    song= a list of lists containing all note(s) of a chord
    chord= points to a single list in the song list of lists
    indexes= points to the single element in the chord list"""
    if index1<0:
        index1=0
    if index2<0:
        index2=0
    if index3<0:
        index3=0
    if index4<0:
        index4=0
    note1=song[chord][index1]
    note2=song[chord][index2]
    note3=song[chord][index3]
    note4=song[chord][index4]
    songfile1='Trimmed Piano Sounds/{}'.format(str(note1)+'(trim).ogg')
    songfile2='Trimmed Piano Sounds/{}'.format(str(note2)+'(trim).ogg')
    songfile3='Trimmed Piano Sounds/{}'.format(str(note3)+'(trim).ogg')
    songfile4='Trimmed Piano Sounds/{}'.format(str(note4)+'(trim).ogg')
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(songfile1))
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(songfile2))
    pygame.mixer.Channel(2).play(pygame.mixer.Sound(songfile3))
    pygame.mixer.Channel(3).play(pygame.mixer.Sound(songfile4))

def getSong(file):
    notes=[]
    with open(file, 'r') as song:
        for line in song:
            if line=="\n":
                continue
            else:
                line=line.strip()
                chord=line.split(',')
                notes.append(chord)
        return notes
    
#the main game loop
Jingle=getSong(JINGLE_BELLS)
Mario=getSong(MARIO)
s_true=getSong(S_TRUE)



def game_loop():
    running=True
    speeds=[0,0,4,5,6,7,8,9,10,11]
##    speeds=[0,0]
    difficulty=30
    # speeds up the game when a multiple of difficulty is met
    global score, possibleX
    ended=False
    numChord=0
    song=s_true
    while running:
        notes=len(song[numChord])
        if score>getHS():
            newHS(score)
        if ended:
            pygame.time.wait(500)
            i=0
            if score>getHS():
                newHS(score)
            show_endScreen()
        for x in range(1,10):
            if score<x*difficulty:
                i=x
                break
        for tile in tileList:
            for deadTile in deadTiles:
                tile.speed=speeds[i]
                deadTile.speed=speeds[i]
        # if the game has ended due to user mistakes, the current score will be recorded
        # and checked against the high score. The end screen will also be shown
        else:
            pass
        show_score()
        show_HS()
        screen.fill(WHITE)
        clock.tick(FPS)
        draw_bg()
        tileList.draw(screen)
        deadTiles.draw(screen)
        # all tiles and text labels are drawn
        new_y=getHighestTile()-tileHeight
        if len(tileList)<5:           
            tile=Tile(BLACK,tileWidth, tileHeight,speeds[i])
            new_x=random.choice(possibleX)
            tile.rect.x=new_x
            tile.rect.y=new_y
            tileList.add(tile)
            # if there are less than 5 tiles in play, a new tile will be created
            # at a random x position, but always one tile higher than the current highest tile
        for deadTile in deadTiles:
            deadTile.deadMove(speeds[i])
        for tile in tileList:
            tile.move(speeds[i])
            # every tile in the list is moved
            if not tile.move(speeds[i]):
                tile.image.fill(RED)
                tileList.draw(screen)
                pygame.display.flip()
                ended=True
                # if the tile reaches the screen boundary, the game ends, and the
                # 'mistake' tile is highlighted in red
        lowestTile=getLowestTile()
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key== pygame.K_ESCAPE:
                    running=False
                if event.type==pygame.QUIT:
                    running=False
                # if the esc button or 'x' button is pressed, the game quits

                # the keys 1, 2, 3, 4 corresponds to the columns from right to left
                # if the lowest tile is indeed in the column as indicated by the user,
                # that tile is coloured grey, and the score is increment
                if event.key==pygame.K_1:
                    if lowestTile.rect.x==0:
                        try:
                            playNote(song,numChord,notes-3,notes-2,notes-2,notes-1)
                            numChord+=1
                            print(numChord)
                        except:
                            numChord=0
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        deadTile=Tile(GREY,tileWidth, tileHeight,speeds[i])
                        deadTile.rect.x=lowestTile.rect.x
                        deadTile.rect.y=lowestTile.rect.y
                        tileList.remove(lowestTile)
                        deadTile.add(deadTiles)
                        score+=1
                    else:
       
                        ended=True
                if event.key==pygame.K_2:
                    if lowestTile.rect.x==tileWidth:
                        try:
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        except:
                            numChord=0
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        deadTile=Tile(GREY,tileWidth, tileHeight,speeds[i])
                        deadTile.rect.x=lowestTile.rect.x
                        deadTile.rect.y=lowestTile.rect.y                   
                        tileList.remove(lowestTile)
                        deadTile.add(deadTiles)
                        score+=1              
                    else:
                        ended=True
                if event.key==pygame.K_3:
                    if lowestTile.rect.x==tileWidth*2:
                        try:
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        except:
                            numChord=0
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        deadTile=Tile(GREY,tileWidth, tileHeight,speeds[i])
                        deadTile.rect.x=lowestTile.rect.x
                        deadTile.rect.y=lowestTile.rect.y                       
                        tileList.remove(lowestTile)
                        deadTile.add(deadTiles)
                        score+=1                        
                    else:
                        ended=True
                if event.key==pygame.K_4:
                    if lowestTile.rect.x==tileWidth*3:
                        try:
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        except:
                            numChord=0
                            playNote(song,numChord,notes-3,notes-2,notes-1)
                            numChord+=1
                        deadTile=Tile(GREY,tileWidth, tileHeight,speeds[i])
                        deadTile.rect.x=lowestTile.rect.x
                        deadTile.rect.y=lowestTile.rect.y                       
                        tileList.remove(lowestTile)
                        deadTile.add(deadTiles)
                        score+=1                                       
                    else:
                        ended=True
        pygame.display.flip()
    pygame.quit()
    quit()
        
  
                    
game_loop()
# Starts the game!


