import numpy as np
import random
from time import *

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
# score parameter
SCORE_LEVEL = 11
SCORE = np.logspace(0, SCORE_LEVEL, SCORE_LEVEL + 1, dtype=np.int64)
# direction
DIRECTION = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))

random.seed(0)


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.candidate_list = []
        self.iterlist = []

    # The input is current chessboard.
    def __printscoretable(self, scoretable):
        self.indent = np.math.log(10 + np.max(scoretable), 10)
        for line in scoretable:
            for element in line:
                print(repr(element).rjust(int(self.indent) // 2 + 3), end=' ')
            print()

    def __printchessboard(self, chessboard):
        print("  ", end=" ")
        for i in range(len(chessboard)):
            if i < 10:
                print(i, end='  ')
            else:
                print(i, end=' ')
        print()
        for i in range(len(chessboard)):
            if i <= 9:
                print(i, end='  ')
            else:
                print(i, end=' ')
            for j in range(len(chessboard[0])):
                if (chessboard[i][j] == -self.color):
                    print(0, end='  ')
                elif (chessboard[i][j] == self.color):
                    print(1, end='  ')
                else:
                    print("  ", end=" ")
            print()

    # calculate octonumber, which helps to judge the pattern
    def __inbound(self, pos):
        a = pos[0]
        b = pos[1]
        if (a >= 0) and (a < self.chessboard_size) and (b >= 0) and (b < self.chessboard_size):
            return True
        return False

    def __nextpos(self, pos, drc, n):
        if type(pos[0]) == np.int64:
            a = pos[0] + n * DIRECTION[drc][0]
            b = pos[1] + n * DIRECTION[drc][1]
        else:
            a = pos[0][0] + n * DIRECTION[drc][0]
            b = pos[1][0] + n * DIRECTION[drc][1]
        return ((a, b))

    def __octonumber(self, chessboard, color, pos, drc):  # color: the color of successive chess need to find
        octonumber = {}
        octonumber['neighbor'] = -2 if not self.__inbound(self.__nextpos(pos, drc, 1)) else color * chessboard[self.__nextpos(pos, drc, 1)]
        octonumber['succ'] = 0
        n = 0
        st = 0
        if octonumber['neighbor'] >= 0:
            st = 2 if octonumber['neighbor'] == 0 else 1
            while (self.__inbound(self.__nextpos(pos, drc, st + n)) and color * chessboard[self.__nextpos(pos, drc, st + n)] == 1):
                n += 1
            octonumber['succ'] = n
        octonumber['outter'] = 0
        if self.__inbound(self.__nextpos(pos, drc, st + n)):
            octonumber['border'] = color * chessboard[self.__nextpos(pos, drc, st + n)]
            # jia 1?
            if (octonumber['border'] == 0 and self.__inbound(self.__nextpos(pos, drc, st + n + 1))):
                # octonumber['border']=2 if chessboard(self.__nextpos(pos,drc,st+n+1))[0]==0 else 1 if color*chessboard[self.__nextpos(pos,drc,st+n)][0]==1 else 0;
                if chessboard[self.__nextpos(pos, drc, st + n + 1)] == 0:
                    octonumber['border'] = 2
                elif (color == chessboard[self.__nextpos(pos, drc, st + n + 1)]):
                    n2 = 1
                    while (self.__inbound(self.__nextpos(pos, drc, st + n + n2 + 1)) and color == chessboard[self.__nextpos(pos, drc, st + n + n2 + 1)]):
                        n2 += 1
                    octonumber['outter'] = n2
                    if ((not self.__inbound(self.__nextpos(pos, drc, st + n + n2 + 1))) or
                            (self.__inbound(self.__nextpos(pos, drc, st + n + n2 + 1)) and
                             chessboard[self.__nextpos(pos, drc, st + n + n2 + 1)] == -color)):
                        octonumber['outter'] = -octonumber['outter']
        else:
            octonumber['border'] = -2  # border: -1,border of board,opposite chess; 0, space; 1,space+1 fri; 2,2space;
        return octonumber

    def __octojudger(self, octo1, octo2, condition1, condition2):
        # octo['neighbor','succ','border','outter']
        if ((octo1['neighbor'] in condition1[0] and octo1['succ'] in condition1[1] and octo1['border'] in condition1[2] and octo1['outter'] in condition1[3] and
             octo2['neighbor'] in condition2[0] and octo2['succ'] in condition2[1] and octo2['border'] in condition2[2] and octo2['outter'] in condition2[3]) or
                (octo1['neighbor'] in condition2[0] and octo1['succ'] in condition2[1] and octo1['border'] in condition2[2] and octo1['outter'] in condition2[3] and
                 octo2['neighbor'] in condition1[0] and octo2['succ'] in condition1[1] and octo2['border'] in condition1[2] and octo2['outter'] in condition1[3])):
            return True
        return False

    def __octojudger2(self, octo, condition):
        if (octo['neighbor'] in condition[0] and octo['succ'] in condition[1] and octo['border'] in condition[2] and octo['outter'] in condition[3]):
            return True
        return False

    def __numofchess(self, chessboard):
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        return len(idx)

    def __numofspace(self, chessboard):
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        return len(idx)

    def __get2dimposition(self, pos1dim):
        return ((pos1dim // self.chessboard_size, pos1dim % self.chessboard_size))

    # score the empty position on the board
    def __score(self, chessboard, thecolor):  ##aspect: 0 for differ chess, 1 for differ chessboard
        idx = np.where(chessboard != COLOR_NONE)
        borderAx = min(idx[0])
        borderBx = max(idx[0])
        borderAy = min(idx[1])
        borderBy = max(idx[1])
        # initiate score table
        scoretable = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int64)
        scoretable[idx] = -1
        # find uncolored positions and score them
        vacancy = list(zip(*np.where(chessboard == COLOR_NONE)))
        # print("vacancy")
        # print(vacancy)
        waytosuccess = [[], []]
        chessboardscore = 0
        for x in vacancy:
            # x is a tuple presenting position of vacant point
            # eight directions octo[which direction 0-7]={neighbor(-1 op or bo,0 vacant,1 fri),succession,border}
            if (x[0] <= borderAx - 3 or x[0] >= borderBx + 3 or x[1] >= borderBy + 3 or x[1] <= borderAy - 3):
                continue
            octo = [[], []]
            if (x[0] == 8 and x[1] == 10):
                asdfwef = 10
            for i in range(8):
                for color in [0, 1]:
                    octo[color].append(self.__octonumber(chessboard, (-2 * color + 1) * thecolor, x, i))
                    # single direction win judge(huo4 chong4 huo3)
            whatever = [-1, 0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
            for color in [0, 1]:  # 0 for attack, 1 for guardian
                numhuoer = nummiansan = 0
                normalsucc = 0
                useless = 0
                nummianer = 0
                nummianyi = 0
                numhuoyi = 0
                for i in range(4):
                    # 1
                    if (((octo[color][i]['neighbor'] == 0 and octo[color][i]['succ'] == 0 and
                          octo[color][i]['border'] != -1 and octo[color][i]['outter'] == 0) or octo[color][i]['neighbor'] == -2) and
                            ((octo[color][i + 4]['neighbor'] == 0 and octo[color][i + 4]['succ'] == 0 and
                              octo[color][i + 4]['border'] != -1 and octo[color][i + 4]['outter'] == 0) or
                             octo[color][i + 4]['neighbor'] == -2)):
                        continue
                    # 2 huosi,chongsi
                    if ((octo[color][i]['neighbor'] == 1 and octo[color][i + 4]['neighbor'] == 1 and octo[color][i]['succ'] + octo[color][i + 4]['succ'] >= 4) or
                            ((octo[color][i]['neighbor'] == 1 and octo[color][i]['succ'] >= 4) or (octo[color][i + 4]['neighbor'] == 1 and octo[color][i + 4]['succ'] >= 4))):
                        scoretable[x] += SCORE[SCORE_LEVEL - color]*1.1
                        chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - color]*1.1
                        if x not in waytosuccess[color]:
                            waytosuccess[color].append(x)
                    # 3 huosan(lian)
                    elif ((octo[color][i]['neighbor'] == 0 and octo[color][i + 4]['neighbor'] == 1 and
                           octo[color][i + 4]['border'] >= 0 and octo[color][i + 4]['succ'] == 3) or
                          (octo[color][i + 4]['neighbor'] == 0 and octo[color][i]['neighbor'] == 1 and octo[color][i]['border'] >= 0 and octo[color][i]['succ'] == 3)):
                        scoretable[x] += SCORE[SCORE_LEVEL - color - 2]
                        chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 2 - color]
                        if x not in waytosuccess[color]:
                            waytosuccess[color].append(x)
                    # 4 huosan(tiao)
                    elif (octo[color][i]['border'] >= 0 and octo[color][i + 4]['border'] >= 0 and
                          octo[color][i]['neighbor'] == octo[color][i + 4]['neighbor'] == 1 and
                          octo[color][i]['succ'] + octo[color][i + 4]['succ'] == 3):
                        scoretable[x] += SCORE[SCORE_LEVEL - color - 2]
                        chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 2 - color]
                        if x not in waytosuccess[color]:
                            waytosuccess[color].append(x)
                    # 5 huoer 1
                    elif (self.__octojudger(octo[color][i], octo[color][i + 4], [[0], [0], whatever, whatever], [[1], [2], [0, 2], whatever]) or
                          self.__octojudger(octo[color][i], octo[color][i + 4], [[0], [0], whatever, whatever], [[0], [2], [0, 2], whatever]) or
                          self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0, 2], whatever], [[1], [1], [0, 2], whatever]) or
                          self.__octojudger(octo[color][i], octo[color][i + 4], [[0], [0], whatever, whatever], [[1], [1], [0], [1]]) or
                          self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0, 2], whatever], [[0], [1], [0, 2], whatever])):
                          numhuoer += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.01
                          if octo[color][i]['neighbor']==1 or octo[color][i+4]['neighbor']==1:
                               scoretable[x] += SCORE[SCORE_LEVEL - color - 7]
                               chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 7 - color]
                    # 10 miansan 1
                            #01111
                    elif   (self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [3], [-1, -2], whatever], [[0], whatever, whatever, whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [2], [-1, -2], whatever], [[1], [1], [0, 2], whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [-1, -2], whatever], [[1], [2], [0, 2], whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [3], [0, 2], whatever], [[-1, -2], [0], whatever, whatever])):
                            scoretable[x] += SCORE[SCORE_LEVEL - color - 6]
                            chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 6 - color]
                            nummiansan += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.01

                            #11_11
                    elif(   self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0], [2, -2]], [whatever, whatever, whatever, whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[0], [2], whatever, whatever], [[1], [1], whatever, whatever]) or
                            #1_111
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[0], [3], whatever, whatever], [whatever, whatever, whatever, whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [2], whatever, whatever], [[0], [1], whatever, whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0], [1, -1]], [[1], [1], whatever, whatever]) or
                            self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [2], [0], [1, -1]], [whatever, whatever, whatever, whatever])):

                            nummiansan += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.01

                    elif (octo[color][i]['succ']+octo[color][i+4]['succ']==2 and (octo[color][i]['border']==-1 or octo[color][i+4]['border']==-1 or octo[color][i]['neighbor']==-1 or octo[color][i+4]['neighbor']==-1)
                            and (not ((octo[color][i]['border']==-1 and octo[color][i]['neighbor']==-1) or (octo[color][i+4]['border']==-1 and octo[color][i+4]['neighbor']==-1)))):
                        nummianer += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.01
                    elif (self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [-1,-2], whatever], [[0], [0], [2], whatever])or
                          self.__octojudger(octo[color][i], octo[color][i + 4], [[0], [1], [-1,-2], whatever], [[0], [0], [2], whatever])):
                          nummianyi += 1
                    elif self.__octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [2], whatever], [[0], [0], whatever, whatever]):
                          numhuoyi += 1

                    # for j in [0,4]:
                    #     if (self.__octojudger2(octo[color][i+j],[[1],[1],[2],whatever])):
                    #         normalsucc+=4
                    #     elif (self.__octojudger2(octo[color][i+j],[[0],[1],[2],whatever])):
                    #         normalsucc+=3
                    #     elif (self.__octojudger2(octo[color][i+j],[[0],[0],[0],[1]])):
                    #         normalsucc+=2
                    #     elif (self.__octojudger2(octo[color][i+j],[[0],[0],[2],[1]])):
                    #         normalsucc+=1
                    #     else:
                    #         useless+=1 if octo[color][i+j]['neighbor']==1 else 0
                if numhuoer + nummiansan >= 1.9 and nummiansan >= 0.9:
                    scoretable[x] += SCORE[SCORE_LEVEL - color - 2]
                    chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 2 - color]

                elif numhuoer >= 1.9 and nummiansan == 0:
                    scoretable[x] += SCORE[SCORE_LEVEL - color - 4]
                    chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 4 - color]

                elif nummianer + numhuoer >=1.9 and nummianer>=0.9:
                    scoretable[x] += SCORE[SCORE_LEVEL - color - 7]
                    chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 7 - color]

                scoretable[x] += ((numhuoyi + nummianer) * SCORE[SCORE_LEVEL - color - 8] + nummianyi * SCORE[SCORE_LEVEL - color - 10])
                chessboardscore += (color * (-2) + 1) * ((numhuoyi + nummianer) * SCORE[SCORE_LEVEL - 8 - color] + nummianyi * SCORE[SCORE_LEVEL - 10 - color])
        # for i in [0,1]:
        #     if len(waytosuccess[i])>1

        # if (normalsucc<10 and normalsucc>=1):
        #     scoretable[x]+=(switch*(-2)+1)*normalsucc*SCORE[SCORE_LEVEL-color-8+switch]
        # elif(normalsucc>=10):
        #     scoretable[x]+=(switch*(-2)+1)*9*SCORE[SCORE_LEVEL-color-8+switch]
        # elif(normalsucc == nummiansan == 0):
        #     scoretable[x]+=(switch*(-2)+1)*useless*SCORE[SCORE_LEVEL-color-10+switch]

        chessboardscore += self.__numofchess(chessboard)
        return ((scoretable, chessboardscore))

    def __statecompare(self, state1, state2, thecolor):
        t = thecolor * self.color  # t=1 find max score,t=-1 find min score
        if t == 1:
            if ((state1['score'] >= 0.9 * SCORE[SCORE_LEVEL] and state2['score'] >= 0.9 * SCORE[SCORE_LEVEL] and state1['iter'] < state2['iter']) or
                    (state1['score'] > state2['score'] >= 0.9 * SCORE[SCORE_LEVEL] and state1['iter'] == state2['iter']) or
                    (state1['score'] >= 0.9 * SCORE[SCORE_LEVEL] > state2['score']) or
                    (0.9 * SCORE[SCORE_LEVEL] > state1['score'] > state2['score'] and state1['score'] > -0.9 * SCORE[SCORE_LEVEL]) or
                    (0.9 * SCORE[SCORE_LEVEL] > state1['score'] == state2['score'] > -0.9 * SCORE[SCORE_LEVEL] and state1['iter'] < state2['iter']) or
                    (state1['score'] <= -0.9 * SCORE[SCORE_LEVEL] and state2['score'] <= -0.9 * SCORE[SCORE_LEVEL] and state1['iter'] > state2['iter']) or
                    (state2['score'] <= state1['score'] <= -0.9 * SCORE[SCORE_LEVEL] and state1['iter'] == state2['iter'])):
                return True
        elif t == -1:
            if ((state1['score'] <= -0.9 * SCORE[SCORE_LEVEL] and state2['score'] <= 0.9 * SCORE[SCORE_LEVEL] and state1['iter'] < state2['iter']) or
                    (state1['score'] < state2['score'] <= -0.9 * SCORE[SCORE_LEVEL] and state1['iter'] == state2['iter']) or
                    (state1['score'] <= -0.9 * SCORE[SCORE_LEVEL] < state2['score']) or
                    (-0.9 * SCORE[SCORE_LEVEL] < state1['score'] < state2['score'] and state1['score'] < 0.9 * SCORE[SCORE_LEVEL]) or
                    (-0.9 * SCORE[SCORE_LEVEL] < state1['score'] == state2['score'] < 0.9 * SCORE[SCORE_LEVEL] and state1['iter'] < state2['iter']) or
                    (state1['score'] >= 0.9 * SCORE[SCORE_LEVEL] and state2['score'] >= 0.9 * SCORE[SCORE_LEVEL] and state1['iter'] < state2['iter']) or
                    (state2['score'] >= state1['score'] >= 0.9 * SCORE[SCORE_LEVEL] and state1['iter'] == state2['iter'])):
                return True
        return False

    def __minmaxdecision(self, chessboard, thecolor, iter, list, ab, ITER, LEVEL):
        if (LEVEL-7*iter)>2 :
            LEVEL -= 7*iter
        elif iter>7:
            LEVEL = 1
        else:
            LEVEL = 2
        max = {'score': -10 * SCORE[SCORE_LEVEL] * self.color * thecolor, 'iter': ITER + 1}
        flag = 0
        score = self.__score(chessboard, -thecolor)
        scoretable = score[0]
        scorechessboard = score[1]
        if iter == 0:
            self.__printscoretable(scoretable)

        pos1dim = np.argsort(-scoretable.reshape((1, self.chessboard_size ** 2))[0])  # sort from big to small
        pos = self.__get2dimposition(pos1dim[0])
        if iter == 0:
            self.candidate_list.append(pos)
        # self.__printscoretable(scoretable)
        # self.candidate_list.append(pos)
        # return
        if (scoretable[pos] >= 0.9*SCORE[SCORE_LEVEL]):
            # self.__printchessboard(chessboard)
            if iter == 0:
                self.iterlist.append(pos)
            return {'score': -scoretable[pos] * thecolor * self.color, 'iter': iter + 1}
        if (iter >= ITER):
            # self.__printchessboard(chessboard)
            if iter == 0:
                self.iterlist.append(pos)
            return {'score': -scorechessboard * thecolor * self.color, 'iter': iter + 1}
        if self.__numofspace(chessboard) == 0:
            return {'score': 0, 'iter': iter + 1}
        else:
            t = 0
            while iter < ITER and t <= len(pos1dim) - 1 and t < LEVEL and scoretable[pos] > 0:
                # print(iter,pos)
                ghostchessboard = chessboard.copy()
                ghostchessboard[pos] = -thecolor
                # self.__printchessboard(ghostchessboard)
                list.append(pos)
                result = self.__minmaxdecision(ghostchessboard, -thecolor, iter + 1, list, max, ITER, LEVEL)
                if pos == (1, 9):
                    asdfas = 234123
                print(list, result)
                list.remove(pos)
                # ABjian zhi
                if (iter >= 1 and ((iter % 2 == 1 and self.__statecompare(ab, result, self.color)) or (iter % 2 == 0 and self.__statecompare(result, ab, self.color)))):
                    t += 1
                    pos = self.__get2dimposition(pos1dim[t])
                    return result
                if flag == 0:
                    max = result
                    flag = 1
                    if iter == 0:
                        self.iterlist.append(pos)
                elif (self.__statecompare(result, max, -thecolor)):
                    max = result
                    if iter == 0:
                        self.iterlist.append(pos)
                t += 1
                pos = self.__get2dimposition(pos1dim[t])
            if t ==0 and scoretable[pos]==0 and iter==0:
                self.iterlist.append(pos)
            return (max)

    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        self.__printchessboard(chessboard)
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        # Empty chessboard
        if len(idx) == self.chessboard_size ** 2:
            self.candidate_list.append((self.chessboard_size // 2, self.chessboard_size // 2))
            return
        # self.__printscoretable(self.__score(chessboard,self.color)[0])
        # Not empty
        # At the early game------puyue
        idx = np.where(chessboard != COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        ""
        if (len(idx)==3 and self.color==1 and chessboard[(7,7)]==chessboard[(9,7)]==-chessboard[(8,8)]==-1):
            self.candidate_list.append((8,7))
            return

        # min max
        if (self.__numofspace(chessboard) == 1):
            pos = np.where(chessboard == 0)
            self.candidate_list.append([pos[0][0], pos[1][0]])
            return

        begin_time = time()

        LEVEL = 8
        MAX_ITER = 9
        if self.__numofchess(chessboard) <= 13:
            LEVEL = 5
            MAX_ITER = 3
        if self.__numofchess(chessboard) >= 110:
            LEVEL = 4
            MAX_ITER = 2

        max = {'score': -10 * SCORE[SCORE_LEVEL], 'iter': 21}
        # Iterative Deepening
        flag = 0
        for ITER in [MAX_ITER]:
            print("ITER: ", ITER)
            begin_time = time()
            self.iterlist.clear()
            result = self.__minmaxdecision(chessboard, -self.color, 0, [],
                                           {'score': 10 * SCORE[SCORE_LEVEL], 'iter': 0}, ITER, LEVEL)
            if flag == 0:
                max = result
                self.candidate_list.append(self.iterlist[-1])
                flag = 1
            elif self.__statecompare(result, max, self.color) and len(self.iterlist) != 0:
                self.candidate_list.append(self.iterlist[-1])
                max = result
            if max['score'] >= 0.9 * SCORE[SCORE_LEVEL]:
                end_time = time()
                print(end_time - begin_time)
                print(self.candidate_list)
                return
            if self.__numofchess(chessboard) <= 12:
                end_time = time()
                print(end_time - begin_time)
                print(self.candidate_list)
                return
            end_time = time()
            print(end_time - begin_time)
        print(self.candidate_list)


def readchessboard(filename, backstep=0):
    file = open(filename)
    str = file.readlines()
    chessboard = np.zeros((15, 15), dtype=np.int)
    if backstep!=0:
        tail = backstep
    else:
        tail = None
    for pos in str[:tail]:
        t = st = 0
        chess = []
        while st < len(pos):
            if pos[st].isnumeric():
                flag = 1
                if st - 1 >= 0 and pos[st - 1] == '-':
                    flag = -1
                if st + 2 <= len(pos) and pos[st:st + 2].isnumeric():
                    chess.append(flag * int(pos[st:st + 2]))
                    st += 3
                else:
                    chess.append(flag * int(pos[st]))
                    st += 2
                t += 1
            else:
                st += 1
        chessboard[chess[0], chess[1]] = chess[2]
    return chessboard


if __name__ == '__main__':
    # begin_time=time()
    chessboard = readchessboard("testcase/chess_log.txt",13)

    agent = AI(15, 1, 5)
    agent.go(chessboard)
