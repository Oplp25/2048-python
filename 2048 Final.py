import pygame,random

blue = (0, 0, 255)
red = (0, 255, 0)
pygame.init()
win = pygame.display.set_mode((640, 700))
pygame.display.set_caption('2048')
pygame.font.init()
myFont = pygame.font.SysFont(None, 100)
titleText = myFont.render('2048', True, (255, 165, 0))
win.blit(titleText, (250, 0))
colourDict={2:'grey',4:'orange',8:(255, 102, 0),16:(252, 177, 3),32:(252, 119, 3),64:(252, 61, 3),128:(169, 252, 3),256:(3, 252, 173),512:(255, 247, 0),1024:(208, 255, 0),2048:(0,255,0)}
pygame.display.update()
pygame.draw.rect(win, blue, (0, 60, 160, 160))
piecesList=[]
gridRefList=[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3]]
class piece(object):
    def __init__(self,startingNum,gridRef):
        self.num=startingNum
        self.gridRef=gridRef
        self.pos=(self.gridRef[0]*160,self.gridRef[1]*160+60)
        self.colour=colourDict[startingNum]
    def move(self,directionMoved):
        hasCollided=False
        atEnd=False
        while not hasCollided and not atEnd:
            if directionMoved=='up':
                self.gridRef[1]-=1
                collisionsTempTup=self.checkCollisions()
                if collisionsTempTup[0]:
                    hasCollided=True
                    self.gridRef[1]+=1
                    self.pieceCollidedWith=collisionsTempTup[1]
                elif self.gridRef[1]==0:
                    atEnd=True
                elif self.gridRef[1]==-1:
                    self.gridRef[1]+=1
                    atEnd=True
            elif directionMoved=='down':
                self.gridRef[1]+=1
                collisionsTempTup=self.checkCollisions()
                if collisionsTempTup[0]:
                    hasCollided=True
                    self.gridRef[1]-=1
                    self.pieceCollidedWith=collisionsTempTup[1]
                elif self.gridRef[1]==3:
                    atEnd=True
                elif self.gridRef[1]==4:
                    self.gridRef[1]-=1
                    atEnd=True
            elif directionMoved=='right':
                self.gridRef[0]+=1
                collisionsTempTup=self.checkCollisions()
                if collisionsTempTup[0]:
                    hasCollided=True
                    self.gridRef[0]-=1
                    self.pieceCollidedWith=collisionsTempTup[1]
                elif self.gridRef[0]==3:
                    atEnd=True
                elif self.gridRef[0]==4:
                    self.gridRef[0]-=1
                    atEnd=True
            elif directionMoved=='left':
                self.gridRef[0]-=1
                collisionsTempTup=self.checkCollisions()
                if collisionsTempTup[0]:
                    hasCollided=True
                    self.gridRef[0]+=1
                    self.pieceCollidedWith=collisionsTempTup[1]
                elif self.gridRef[0]==0:
                    atEnd=True
                elif self.gridRef[0]==-1:
                    self.gridRef[0]+=1
                    atEnd=True
            if hasCollided and self.num==self.pieceCollidedWith.num:
                self.combine(directionMoved,self.pieceCollidedWith)
    def checkCollisions(self):
        for i in piecesList:
            if i.gridRef==self.gridRef and not i==self:
                return [True,i]
        return [False]
    def combine(self,direction,pieceCol):
        if direction=='right':
            if self.gridRef[0]==3:
                piecesList.append(piece(self.num*2,self.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
            else:
                piecesList.append(piece(self.num*2,pieceCol.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
        if direction=='left':
            if self.gridRef[0]==0:
                piecesList.append(piece(self.num*2,self.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
            else:
                piecesList.append(piece(self.num*2,pieceCol.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
        if direction=='down':
            if self.gridRef[1]==3:
                piecesList.append(piece(self.num*2,self.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
            else:
                piecesList.append(piece(self.num*2,pieceCol.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
        if direction=='up':
            if self.gridRef[1]==0:
                piecesList.append(piece(self.num*2,self.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
            else:
                piecesList.append(piece(self.num*2,pieceCol.gridRef))
                piecesList.remove(self)
                piecesList.remove(pieceCol)
    def draw(self):
        self.pos=(self.gridRef[0]*160+10,self.gridRef[1]*160+70)
        text=myFont.render(str(self.num), True, (0, 0, 0))
        pygame.draw.rect(win,self.colour,(self.pos[0],self.pos[1],140,140))
        win.blit(text,[self.pos[0]+50,self.pos[1]+40])
def drawGrid():
    x = 0
    y = 60
    for i in range(4):
        for g in range(4):
            if g == 0 or g == 2:
                pygame.draw.rect(win, blue, (x, y, 160, 160))
            else:
                pygame.draw.rect(win, red, (x, y, 160, 160))
            x+=160
        if i==0 or i==2:
            x=-160
        else:
            pygame.draw.rect(win, blue, (x, y, 160, 160))
            x=0
            
        y+=160
def prioritySet(direction):
    priorityList=[]
    for i in range(16):
        priorityList.append('')
    if direction=='right':
        for i in piecesList:
            if i.gridRef[0]==3:
                priorityList[i.gridRef[1]]=i
            elif i.gridRef[0]==2:
                priorityList[i.gridRef[1]+4]=i
            elif i.gridRef[0]==1:
                priorityList[i.gridRef[1]+8]=i
            else:
                priorityList[i.gridRef[1]+12]=i
    elif direction=='left':
        for i in piecesList:
            if i.gridRef[0]==0:
                priorityList[i.gridRef[1]]=i
            if i.gridRef[0]==1:
                priorityList[i.gridRef[1]+4]=i
            if i.gridRef[0]==2:
                priorityList[i.gridRef[1]+8]=i
            else:
                priorityList[i.gridRef[1]+12]=i
    elif direction=='up':
        for i in piecesList:
            if i.gridRef[1]==0:
                priorityList[i.gridRef[0]]=i
            if i.gridRef[1]==1:
                priorityList[i.gridRef[0]+4]=i
            if i.gridRef[1]==2:
                priorityList[i.gridRef[0]+8]=i
            else:
                priorityList[i.gridRef[0]+12]=i
    elif direction=='down':
        for i in piecesList:
            if i.gridRef[1]==3:
                priorityList[i.gridRef[0]]=i
            if i.gridRef[1]==2:
                priorityList[i.gridRef[0]+4]=i
            if i.gridRef[1]==1:
                priorityList[i.gridRef[0]+8]=i
            else:
                priorityList[i.gridRef[0]+12]=i
    while '' in priorityList: priorityList.remove('')
    return priorityList
def gameOver():
    pygame.quit()
    print('Game Over')
    run=False
def draw():
    drawGrid()
    for i in piecesList:
        i.draw()
    pygame.display.update()
#starting piece
def spawnPiece():
    startingNum=random.choices((2,4),(0.7,0.3))
    startingNum=int(startingNum[0])
    availableGridRef=[[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3]]
    for i in piecesList:
        availableGridRef.remove(i.gridRef)
    try:
        piecesList.append(piece((startingNum),random.choice(availableGridRef)))
    except IndexError:
        gameOver()
        exit()
spawnPiece()
run = True
while run:
    draw()
    for i in piecesList:
        if i.gridRef==2048:
            print('you win!')
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                currentPriorityList=prioritySet('right')
                for i in currentPriorityList:
                    i.move('right')
                spawnPiece()
            elif event.key==pygame.K_LEFT:
                currentPriorityList=prioritySet('left')
                for i in currentPriorityList:
                    i.move('left')
                spawnPiece()
            elif event.key==pygame.K_DOWN:
                currentPriorityList=prioritySet('down')
                for i in currentPriorityList:
                    i.move('down')
                spawnPiece()
            elif event.key==pygame.K_UP:
                currentPriorityList=prioritySet('up')
                for i in currentPriorityList:
                    i.move('up')
                spawnPiece()
            #temp event-test spawnPiece
            if event.key==pygame.K_SPACE:
                spawnPiece()              
