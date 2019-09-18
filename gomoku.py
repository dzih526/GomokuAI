import numpy as np
import random
from time import *

COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
#score parameter
SCORE_LEVEL=12
SCORE = np.logspace(0,SCORE_LEVEL,SCORE_LEVEL+1,dtype=np.int64)
#direction
DIRECTION=((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1))
ITER=4
LEVEL=4

random.seed(0)
#don't change the class name
class AI(object):
    #chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        #You are white or black
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        # self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your candidate_list as your decision .
        self.candidate_list = []
        self.ab=[-10*SCORE[SCORE_LEVEL]]*ITER
# The input is current chessboard.
    def __printscoretable(self,scoretable):
        for line in scoretable:
            for element in line:
                print(repr(element).rjust(int(self.indent)+5),end=' ')
            print()
    def __printchessboard(self,chessboard):
        print("  ",end=" ")
        for i in range(len(chessboard)):
            if i<10:
                print(i,end='  ')
            else:
                print(i,end=' ')
        print()
        for i in range(len(chessboard)):
            print(i,end='  ')
            for j in range(len(chessboard[0])):
                if(chessboard[i][j]==-self.color):
                    print(0,end='  ')
                elif (chessboard[i][j]==self.color):
                    print(1,end='  ')
                else:
                    print("  ",end=" ")
            print()
    #calculate octonumber, which helps to judge the pattern
    def __inbound(self,pos):
        a=pos[0][0]
        b=pos[1][0]
        if ((a>=0)and(a<self.chessboard_size)and(b>=0)and(b<self.chessboard_size)):
            return True
        return False
    def __nextpos(self,pos,drc,n):
        if type(pos[0])==np.int64 :
            a=pos[0]+n*DIRECTION[drc][0]
            b=pos[1]+n*DIRECTION[drc][1]
        else:
            a=pos[0][0]+n*DIRECTION[drc][0]
            b=pos[1][0]+n*DIRECTION[drc][1]
        return (([a],[b]))
    def __octonumber(self,chessboard,color,pos,drc):#color: the color of successive chess need to find
        octonumber={}
        octonumber['neighbor'] = -2 if not self.__inbound(self.__nextpos(pos,drc,1)) else color*chessboard[self.__nextpos(pos,drc,1)][0]
        octonumber['succ']=0
        n = 0
        st = 0
        if octonumber['neighbor']>=0:
            st = 2 if octonumber['neighbor'] == 0 else 1
            while (self.__inbound(self.__nextpos(pos,drc,st+n)) and color*chessboard[self.__nextpos(pos,drc,st+n)][0]==1):
                n+=1
            octonumber['succ']=n
        octonumber['outter']=0
        if self.__inbound(self.__nextpos(pos,drc,st+n)):
            octonumber['border']=color*chessboard[self.__nextpos(pos,drc,st+n)][0]
            # jia 1?
            if (octonumber['border']==0 and self.__inbound(self.__nextpos(pos,drc,st+n+1))):
                # octonumber['border']=2 if chessboard(self.__nextpos(pos,drc,st+n+1))[0]==0 else 1 if color*chessboard[self.__nextpos(pos,drc,st+n)][0]==1 else 0;
                if chessboard[self.__nextpos(pos,drc,st+n+1)][0]==0:
                    octonumber['border']=2
                elif (color == chessboard[self.__nextpos(pos,drc,st+n+1)][0]):
                    n2=1
                    while (self.__inbound(self.__nextpos(pos,drc,st+n+n2+1))and color==chessboard[self.__nextpos(pos,drc,st+n+n2+1)][0]):
                        n2+=1
                    octonumber['outter']=n2
                    if ((not self.__inbound(self.__nextpos(pos,drc,st+n+n2+1)) )or
                       (self.__inbound(self.__nextpos(pos,drc,st+n+n2+1)) and chessboard[self.__nextpos(pos,drc,st+n+n2+1)][0]==-color)):
                        octonumber['outter']=-octonumber['outter']
        else:
            octonumber['border']=-2#border: -1,border of board,opposite chess; 0, space; 1,space+1 fri; 2,2space;
        return octonumber
    def __octojudger(self,octo1,octo2,condition1,condition2):
        #octo['neighbor','succ','border','outter']
        if ((octo1['neighbor'] in condition1[0] and octo1['succ'] in condition1[1] and octo1['border'] in condition1[2] and octo1['outter'] in condition1[3] and
             octo2['neighbor'] in condition2[0] and octo2['succ'] in condition2[1] and octo2['border'] in condition2[2] and octo2['outter'] in condition2[3]) or
            (octo1['neighbor'] in condition2[0] and octo1['succ'] in condition2[1] and octo1['border'] in condition2[2] and octo1['outter'] in condition2[3] and
             octo2['neighbor'] in condition1[0] and octo2['succ'] in condition1[1] and octo2['border'] in condition1[2] and octo2['outter'] in condition1[3])):
            return True
        return False
    def __octojudger2(self,octo,condition):
        if (octo['neighbor'] in condition[0] and octo['succ'] in condition[1] and octo['border'] in condition[2] and octo['outter'] in condition[3]):
            return True
        return False
    def __numofchess(self,chessboard):
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        return len(idx)
    def __get2dimposition(self,pos1dim):
        return ((pos1dim//self.chessboard_size,pos1dim%self.chessboard_size))

# score the empty position on the board
    def __score(self, chessboard, thecolor, aspect=0): ##aspect: 0 for differ chess, 1 for differ chessboard
        idx = np.where(chessboard != COLOR_NONE)
        # initiate score table
        scoretable = np.zeros((self.chessboard_size,self.chessboard_size),dtype=np.int64)
        scoretable[idx]=-1
        # find uncolored positions and score them
        vacancy = list(zip(*np.where(chessboard == COLOR_NONE)))
        # print("vacancy")
        # print(vacancy)
        for x in vacancy:
            #x is a tuple presenting position of vacant point
            #eight directions octo[which direction 0-7]={neighbor(-1 op or bo,0 vacant,1 fri),succession,border}
            octo=[[],[]]
            if(x[0]==3 and x[1]==6):
                asdfwef=10
            for i in range(8):
                for color in [0,1]:
                    octo[color].append(self.__octonumber(chessboard,(-2*color+1)*thecolor,x,i))
                    # single direction win judge(huo4 chong4 huo3)
            whatever=[-1,0,1,2,3,4,5,-1,-2,-3,-4,-5]
            for color in [0,1]:#0 for attack, 1 for guardian
                numhuoer=nummiansan=0
                normalsucc=0
                useless=0
                switch=1 if (aspect==1 and color==1) else 0
                for i in range(4):
                    #1
                    if (((octo[color][i]['neighbor']==0 and octo[color][i]['succ']==0 and octo[color][i]['border']!=-1 and octo[color][i]['outter']==0) or octo[color][i]['neighbor']==-2) and
                        ((octo[color][i+4]['neighbor']==0 and octo[color][i+4]['succ']==0 and octo[color][i+4]['border']!=-1 and octo[color][i+4]['outter']==0)or octo[color][i+4]['neighbor']==-2)):
                        continue
                    #2 huosi,chongsi
                    if ((octo[color][i]['neighbor']==1 and octo[color][i+4]['neighbor']==1 and octo[color][i]['succ'] + octo[color][i+4]['succ']>=4)or
                       ((octo[color][i]['neighbor']==1 and octo[color][i]['succ']==4)or
                        (octo[color][i+4]['neighbor']==1 and octo[color][i+4]['succ']==4))):
                        scoretable[x]+=(switch*(-2)+1)*SCORE[SCORE_LEVEL-color+switch]
                        continue
                    #3 huosan(lian)
                    if ((octo[color][i]['neighbor']==0 and octo[color][i+4]['neighbor']==1 and octo[color][i+4]['border']>=0 and octo[color][i+4]['succ']==3) or
                        (octo[color][i+4]['neighbor']==0 and octo[color][i]['neighbor']==1 and octo[color][i]['border']>=0 and octo[color][i]['succ']==3)):
                        scoretable[x]+=(switch*(-2)+1)*SCORE[SCORE_LEVEL-color-2+switch]
                        continue
                    #4 huosan(tiao)
                    if (octo[color][i]['border']>=0 and octo[color][i+4]['border']>=0 and
                        octo[color][i]['neighbor']==octo[color][i+4]['neighbor']==1 and
                        octo[color][i]['succ']+octo[color][i+4]['succ']==3):
                        scoretable[x]+=(switch*(-2)+1)*SCORE[SCORE_LEVEL-color-2+switch]
                        continue

                    #5 huoer 1
                    if (self.__octojudger(octo[color][i],octo[color][i+4],[[0],[0],[0,2],whatever],[[1],[2],[0,2],whatever]) or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[0],whatever,whatever],[[0],[2],[0,2],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[2],whatever],[[1],[1],[2],whatever]) or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[0],whatever,whatever],[[1],[1],[0],[1]]) or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0,2],whatever],[[0],[1],[0,2],whatever])
                        ):
                        numhuoer+=1+(octo[color][i]['neighbor']+octo[color][i+4]['neighbor'])*0.01

                    #10 miansan 1
                    elif (self.__octojudger(octo[color][i],octo[color][i+4],[[1],[3],[-1,-2],whatever],[[0],whatever,whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[-1,-2],whatever],[[1],[1],[0],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[-1,-2],whatever],[[1],[2],[0],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[3],[0],whatever],[[-1,-2],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[3],whatever,whatever],[[-1,-2],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[1],[-1,-2],whatever],[[1],[2],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[-1]],[[1],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[-1]],[whatever,whatever,whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[2,-2]],[[-1,-2],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[2],[0],whatever],[[1],[1],[-1,-2],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[2],[-1,-2],whatever],[[1],[1],[0],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[1,-1]],[[-1,-2],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[-2]],[[0],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[1,-1]],[[-1,-2],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[-1,-2],whatever],[[1],[1],[0],[1,-1]])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[-1,-2],whatever],[[0],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[3],[-1,-2],whatever],[whatever,whatever,whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[2,-2]],[[0],[0],whatever,whatever]) or                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[2],whatever,whatever],[[1],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[3],whatever,whatever],[whatever,whatever,whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],whatever,whatever],[[0],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[1,-1]],[[1],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[1,-1]],[whatever,whatever,whatever,whatever])):
                        nummiansan+=1+(octo[color][i]['neighbor']+octo[color][i+4]['neighbor'])*0.01

                    for j in [0,4]:
                        if (self.__octojudger2(octo[color][i+j],[[1],[1],[2],whatever])):
                            normalsucc+=4
                        elif (self.__octojudger2(octo[color][i+j],[[0],[1],[2],whatever])):
                            normalsucc+=3
                        elif (self.__octojudger2(octo[color][i+j],[[0],[0],[0],[1]])):
                            normalsucc+=2
                        elif (self.__octojudger2(octo[color][i+j],[[0],[0],[2],[1]])):
                            normalsucc+=1
                        else:
                            useless+=1 if octo[color][i+j]['neighbor']==1 else 0



                if (numhuoer+nummiansan>=1.9 and nummiansan>=0.9):
                    scoretable[x]+=(switch*(-2)+1)*SCORE[SCORE_LEVEL-color-2+switch]
                elif(numhuoer>=1.9 and nummiansan==0):
                    scoretable[x]+=(switch*(-2)+1)*SCORE[SCORE_LEVEL-color-4+switch]
                elif(nummiansan==0 or numhuoer==0):
                    scoretable[x]+=(switch*(-2)+1)*(numhuoer+nummiansan)*SCORE[SCORE_LEVEL-color-6+switch]

                if (normalsucc<10 and normalsucc>=1):
                    scoretable[x]+=(switch*(-2)+1)*normalsucc*SCORE[SCORE_LEVEL-color-8+switch]
                elif(normalsucc>=10):
                    scoretable[x]+=(switch*(-2)+1)*9*SCORE[SCORE_LEVEL-color-8+switch]
                elif(normalsucc == nummiansan == 0):
                    scoretable[x]+=(switch*(-2)+1)*useless*SCORE[SCORE_LEVEL-color-10+switch]



        #
        return (scoretable)
    def __scorechessboard(self,chessboard,thecolor):
        return (np.sum(self.__score(chessboard,thecolor,1))+self.__numofchess(chessboard))
    def __statecompare(self,state1,state2,thecolor):
        if ((state1['state']==state2['state']=='win' and state1['color']==-thecolor and state2['color']==thecolor)or
            (state1['state']==state2['state']=='win' and state1['color']==state2['color']==-thecolor and state1['iter']<state2['iter'])or
            (state1['state']==state2['state']=='win' and state1['color']==state2['color']==-thecolor and state1['iter']==state2['iter'] and state1['score']<state2['score'])or
            (state1['state']=='win' and state1['color']==-thecolor and state2['state']=='ongo')or
            (state1['state']==state2['state']=='ongo' and state1['score']>state2['score'])or
            (state2['state']=='win' and state2['color']==thecolor and state1['state']=='ongo')or
            (state1['state']=='ongo' and state2['state']=='win' and state2['color']==thecolor)or
            (state1['state']==state2['state']=='win' and state1['color']==state2['color']==thecolor and state1['score']>state2['score'])):
            return True
        return False

    def __minmaxdecision(self,chessboard,thecolor,iter):
        max={'state':'win','color':thecolor,'score':-20*SCORE[SCORE_LEVEL],'iter':ITER+1}
        scoretable = self.__score(chessboard,-thecolor)
        # print("________",self.__scorechessboard(chessboard,-thecolor),self.__scorechessboard(chessboard,thecolor))
        pos1dim = np.argsort(-scoretable.reshape((1,self.chessboard_size**2))[0])
        pos = self.__get2dimposition(pos1dim[0])
        # if (pos[0]==3 and pos[1]==11):
        #     asfsd=1232
        # print(chessboard)
        if (scoretable[pos]>=SCORE[SCORE_LEVEL] or iter+1>=ITER):
            # self.__printchessboard(chessboard)
            if iter==0:
                self.candidate_list.append(pos)
            # self.ab[iter]=self.__scorechessboard(chessboard,-thecolor)
            state='win' if scoretable[pos]>=SCORE[SCORE_LEVEL] else 'ongo'
            return ({'state':state,'color':-thecolor,'score':self.ab[iter],'iter':iter+1})
        else:
            t = 0
            while (iter+1 < ITER and t<=len(pos1dim)-1 and t<LEVEL and scoretable[pos]>0):
                # print(iter,pos)
                ghostchessboard = chessboard.copy()
                ghostchessboard[pos]=-thecolor
                result=self.__minmaxdecision(ghostchessboard,-thecolor,iter+1)
                #ABjian zhi
                if (iter>1 and (-result['score']*(self.color*thecolor))<self.ab[iter-1]):
                    continue
                if (self.__statecompare(result,max,thecolor)):
                    max=result
                    self.ab[iter]=max['score']
                    if iter==0:
                        self.candidate_list.append(pos)
                t+=1
                pos=self.__get2dimposition(pos1dim[t])
            return (max)



    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        # print("chessboard")
        # self.__printchessboard(chessboard)
        #==================================================================
        #Write your algorithm here
        #Here is the simplest sample:Random decision
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        #Empty chessboard
        if len(idx)==self.chessboard_size**2:
            self.candidate_list.append((self.chessboard_size//2,self.chessboard_size//2))
            return
        #Not empty
        #At the early game------puyue
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        ""
        if len(idx)==2:
            me = np.where(chessboard == self.color)
            opponent = np.where(chessboard == -self.color)
            a=opponent[0][0]-me[0][0]
            b=opponent[1][0]-me[1][0]
            if a==0:
                x=0
                y=b
            else:
                y=int(((a**4+(a**2)*b**2)/(a**2+b**2))**(1/2))
                x=int(b*y/a)
                if (a*x+b*y!=0):
                    x=-x
            if chessboard[me[0][0]+int(x)][me[1][0]+int(y)]==COLOR_NONE:
                self.candidate_list.append((me[0][0]+x,me[1][0]+y))
                return

        #min max


        self.__minmaxdecision(chessboard,-self.color,0)
        print(self.candidate_list)
        # self.indent=np.math.log(10+np.max(scoretable),10)
        # print("scoretable")
        # self.__printscoretable(scoretable)

        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        # assert chessboard[self.candidate_list[-1][0],self.candidate_list[-1][1]]== COLOR_NONE

        #Add your decision into candidate_list, Records the chess board
def readchessboard(filename,backstep=0):
    file = open(filename)
    str = file.readlines()
    chessboard = np.zeros((15,15), dtype=np.int)
    tail=None if backstep==0 else -backstep
    for pos in str[:tail]:
        t=st=0
        chess=[]
        while st < len(pos):
            if pos[st].isnumeric():
                flag=1
                if st-1>=0 and pos[st-1]=='-':
                    flag=-1
                if st+2<=len(pos) and pos[st:st+2].isnumeric():
                    chess.append(flag*int(pos[st:st+2]))
                    st+=3
                else:
                    chess.append(flag*int(pos[st]))
                    st+=2
                t+=1
            else:
                st+=1
        chessboard[chess[0],chess[1]]=chess[2]
    return chessboard

if __name__ == '__main__':
    begin_time=time()
    chessboard = readchessboard("testcase/chess_log14.txt")
    agent=AI(15,1,5)
    agent.go(chessboard)
    print(agent.candidate_list)
    end_time=time()
    print(end_time-begin_time)