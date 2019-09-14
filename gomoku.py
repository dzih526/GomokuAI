import numpy as np
import random


COLOR_BLACK=-1
COLOR_WHITE=1
COLOR_NONE=0
#score parameter
SCORE_LEVEL=6
SCORE = np.logspace(0,SCORE_LEVEL,SCORE_LEVEL+1,dtype=np.int64)
#direction
DIRECTION=((-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1))


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
# The input is current chessboard.

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
        octonumber['neighbor'] = -1 if not self.__inbound(self.__nextpos(pos,drc,1)) else color*chessboard[self.__nextpos(pos,drc,1)][0]
        octonumber['succ']=0
        n = 0
        st = 0
        if octonumber['neighbor']!=-1:
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
                    if (not self.__inbound(self.__nextpos(pos,drc,st+n+n2+1)) or
                       (self.__nextpos(pos,drc,st+n+n2+1) and chessboard[self.__nextpos(pos,drc,st+n+n2+1)][0]==-1)):
                        octonumber['outter']=-octonumber['outter'];
        else:
            octonumber['border']=-1#border: -1,border of board,opposite chess; 0, space; 1,space+1 fri; 2,2space;
        return octonumber
    def __octojudger(self,octo1,octo2,condition1,condition2):
        #octo['neighbor','succ','border','outter']
        if ((octo1['neighbor'] in condition1[0] and
             octo1['succ'] in condition1[1] and
             octo1['border'] in condition1[2] and
             octo1['outter'] in condition1[3] and
             octo2['neighbor'] in condition2[0] and
             octo2['succ'] in condition2[1] and
             octo2['border'] in condition2[2] and
             octo2['outter'] in condition2[3]) or
            (octo1['neighbor'] in condition2[0] and
             octo1['succ'] in condition2[1] and
             octo1['border'] in condition2[2] and
             octo1['outter'] in condition2[3] and
             octo2['neighbor'] in condition1[0] and
             octo2['succ'] in condition1[1] and
             octo2['border'] in condition1[2] and
             octo2['outter'] in condition1[3])):
            return True
        return False

# score the empty position on the board
    def __score(self,chessboard):
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
            for i in range(8):
                for color in [0,1]:
                    octo[color].append(self.__octonumber(chessboard,(-2*color+1)*self.color,x,i))
                    # single direction win judge(huo4 chong4 huo3)
            whatever=[-1,0,1,2,3,4,5,-1,-2,-3,-4,-5]
            for color in [0,1]:
                numhuoer=nummiansan=0
                for i in range(4):
                    #1
                    if (octo[color][i]['neighbor']== octo[color][i+4]['neighbor']==0):
                        continue
                    #2 huosi,chongsi
                    if (octo[color][i]['succ'] + octo[color][i+4]['succ']>=4):
                        scoretable[x]+=SCORE[SCORE_LEVEL-color]
                        continue
                    #3 huosan(lian)
                    if ((octo[color][i]['neighbor']==0 and octo[color][i+4]['border']>=0 and octo[color][i+4]['succ']==3) or
                        (octo[color][i+4]['neighbor']==0 and octo[color][i]['border']>=0 and octo[color][i]['succ']==3)):
                        scoretable[x]+=SCORE[SCORE_LEVEL-color-1]
                        continue
                    #4 huosan(tiao)
                    if (octo[color][i]['border']>=0 and octo[color][i+4]['border']>=0 and
                        octo[color][i]['neighbor']==octo[color][i+4]['neighbor']==1 and
                        octo[color][i]['succ']+octo[color][i+4]['succ']==3):
                        scoretable[x]+=SCORE[SCORE_LEVEL-color-1]
                        continue

                    #5 huoer 1
                    if (self.__octojudger(octo[color][i],octo[color][i+4],[[0],[0],[0],whatever],[[1],[2],[2],whatever]) or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[0],whatever,whatever],[[0],[2],[0,2],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[2],whatever],[[1],[1],[2],whatever]) or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[1],[0],whatever],[[1],whatever,[0],whatever]) or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[1]],[[0],[0],whatever,whatever])
                        ):
                        numhuoer+=1
                        continue
                    #10 miansan 1
                    if (self.__octojudger(octo[color][i],octo[color][i+4],[[1],[3],[-1],whatever],[[0],whatever,whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[-1],whatever],[[1],[1],[0],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[-1],whatever],[[1],[2],[0],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[3],[0],whatever],[[-1],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[3],whatever,whatever],[[-1],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[1],[-1],whatever],[[1],[2],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[-1]],[[1],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[-1]],[whatever,whatever,whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[2,-2]],[[-1],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[2],[0],whatever],[[1],[1],[-1],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[2],[-1],whatever],[[1],[1],[0],whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[1,-1]],[[-1],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[0],[-2]],[[0],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[0],[1,-1]],[[-1],[0],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[1],[-1],whatever],[[1],[1],[0],[1,-1]])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[1],[2],[-1],whatever],[[0],[1],whatever,whatever])or
                        self.__octojudger(octo[color][i],octo[color][i+4],[[0],[3],[-1],whatever],[whatever,whatever,whatever,whatever])):
                        nummiansan+=1
                        continue
                if (numhuoer+nummiansan>=2):
                    scoretable[x]+=SCORE[SCORE_LEVEL-color-1]
                elif(numhuoer+nummiansan==1):
                    scoretable[x]+=SCORE[numhuoer+nummiansan]
                normalsucc=octo[color][i]['succ']+abs(octo[color][i]['outter'])+octo[color][i+4]['succ']+abs(octo[color][i+4]['outter'])
                if (normalsucc<SCORE_LEVEL-color-2 and normalsucc>=1):
                    scoretable[x]+=SCORE[normalsucc]


        print("scoretable")
        print(scoretable)
        #
        return (scoretable)



    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        print("chessboard")
        print(chessboard)
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
        scoretable=self.__score(chessboard)
        new_pos = list(zip(*(np.where(scoretable == np.max(scoretable)))))[0]


        #==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        #If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]== COLOR_NONE
        #Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
# if __name__ == '__main__':
#     chessboard = np.zeros((15,15), dtype=np.int)
#     chessboard[2, 2] = 1
#     chessboard[3, 3] = 1
#     chessboard[4, 4] = 1
#     chessboard[5, 6] = 1
#     chessboard[5, 8] = 1
#     chessboard[1:3, 11] = -1
#     chessboard[3, 9:11] = -1
#     chessboard[6, 13] = -1
#     agent=AI(15,-1,5)
#     agent.go(chessboard)
#     print(agent.candidate_list)