import numpy as np
import random
from time import *

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
# score parameter
SCORE_LEVEL = 10
SCORE = np.logspace(0, SCORE_LEVEL, SCORE_LEVEL + 1, dtype=np.int64)
# direction
DIRECTION = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
whatever = [-1, 0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
random.seed(0)
def octojudger( octo1, octo2, condition1, condition2):
    # octo['neighbor','succ','border','outter']
    if ((octo1['neighbor'] in condition1[0] and octo1['succ'] in condition1[1] and octo1['border'] in condition1[2] and octo1['outter'] in condition1[3] and
         octo2['neighbor'] in condition2[0] and octo2['succ'] in condition2[1] and octo2['border'] in condition2[2] and octo2['outter'] in condition2[3]) or
        (octo1['neighbor'] in condition2[0] and octo1['succ'] in condition2[1] and octo1['border'] in condition2[2] and octo1['outter'] in condition2[3] and
         octo2['neighbor'] in condition1[0] and octo2['succ'] in condition1[1] and octo2['border'] in condition1[2] and octo2['outter'] in condition1[3])):
        return True
    return False

octo=[]
octo.append([{'neighbor': -1, 'succ': 0, 'outter': 0, 'border': 0}, {'neighbor': 0, 'succ': 0, 'outter': 0, 'border': 2}, {'neighbor': 0, 'succ': 0, 'outter': 0, 'border': -1}, {'neighbor': 0, 'succ': 0, 'outter': 0, 'border': -1}, {'neighbor': 1, 'succ': 2, 'outter': 0, 'border': -1}, {'neighbor': -1, 'succ': 0, 'outter': 0, 'border': 0}, {'neighbor': -1, 'succ': 0, 'outter': 0, 'border': 0}, {'neighbor': -1, 'succ': 0, 'outter': 0, 'border': 0}])
octo.append([{'neighbor': 1, 'succ': 1, 'outter': 0, 'border': -1},
             {'neighbor': 0, 'succ': 0, 'outter': 0, 'border': 2},
             {'neighbor': 0, 'succ': 2, 'outter': 0, 'border': 2},
             {'neighbor': 0, 'succ': 1, 'outter': 0, 'border': 2},
             {'neighbor': -1, 'succ': 0, 'outter': 0, 'border': 0},
             {'neighbor': 1, 'succ': 1, 'outter': 0, 'border': -1},
             {'neighbor': 1, 'succ': 1, 'outter': 0, 'border': 2},
             {'neighbor': 1, 'succ': 2, 'outter': 0, 'border': 0}])
scoretable = np.zeros((15, 15), dtype=np.int64)
chessboardscore=0
x=(5,8)
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
            scoretable[x] += SCORE[SCORE_LEVEL - color]
            chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - color]

        # 3 huosan(lian)
        elif ((octo[color][i]['neighbor'] == 0 and octo[color][i + 4]['neighbor'] == 1 and
               octo[color][i + 4]['border'] >= 0 and octo[color][i + 4]['succ'] == 3) or
              (octo[color][i + 4]['neighbor'] == 0 and octo[color][i]['neighbor'] == 1 and octo[color][i]['border'] >= 0 and octo[color][i]['succ'] == 3)):
            scoretable[x] += SCORE[SCORE_LEVEL - color - 2]
            chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 2 - color]

        # 4 huosan(tiao)
        elif (octo[color][i]['border'] >= 0 and octo[color][i + 4]['border'] >= 0 and
              octo[color][i]['neighbor'] == octo[color][i + 4]['neighbor'] == 1 and
              octo[color][i]['succ'] + octo[color][i + 4]['succ'] == 3):
            scoretable[x] += SCORE[SCORE_LEVEL - color - 2]
            chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 2 - color]

        # 5 huoer 1
        elif (octojudger(octo[color][i], octo[color][i + 4], [[0], [0], whatever, whatever], [[1], [2], [0, 2], whatever]) or
              octojudger(octo[color][i], octo[color][i + 4], [[0], [0], whatever, whatever], [[0], [2], [0, 2], whatever]) or
              octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0, 2], whatever], [[1], [1], [0, 2], whatever]) or
              octojudger(octo[color][i], octo[color][i + 4], [[0], [0], whatever, whatever], [[1], [1], [0], [1]]) or
              octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0, 2], whatever], [[0], [1], [0, 2], whatever])):
            numhuoer += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.01

        # 10 miansan 1
                #01111
        if      (octojudger(octo[color][i], octo[color][i + 4], [[1], [3], [-1, -2], whatever], [[0], whatever, whatever, whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[1], [2], [-1, -2], whatever], [[1], [1], [0, 2], whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [-1, -2], whatever], [[1], [2], [0, 2], whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[1], [3], [0, 2], whatever], [[-1, -2], [0], whatever, whatever]) or
                #11_11
                octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0], [2, -2]], [whatever, whatever, whatever, whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[0], [2], whatever, whatever], [[1], [1], whatever, whatever]) or
                #1_111
                octojudger(octo[color][i], octo[color][i + 4], [[0], [3], whatever, whatever], [whatever, whatever, whatever, whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[1], [2], whatever, whatever], [[0], [1], whatever, whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [0], [1, -1]], [[1], [1], whatever, whatever]) or
                octojudger(octo[color][i], octo[color][i + 4], [[1], [2], [0], [1, -1]], [whatever, whatever, whatever, whatever])):

                nummiansan += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.01

        elif (octo[color][i]['succ']+octo[color][i+4]['succ']==2 and (octo[color][i]['border']==-1 or octo[color][i+4]['border']==-1 or octo[color][i]['neighbor']==-1 or octo[color][i+4]['neighbor']==-1)):
            nummianer += 1 + (octo[color][i]['neighbor'] + octo[color][i + 4]['neighbor']) * 0.1
        elif octojudger(octo[color][i], octo[color][i + 4], [[-1,-2], [0], whatever, whatever], [[0], [0], [2], whatever]):
            nummianyi += 1
        elif octojudger(octo[color][i], octo[color][i + 4], [[1], [1], [2], whatever], [[0], [0], whatever, whatever]):
            numhuoyi += 1

        # for j in [0,4]:
        #     if (octojudger2(octo[color][i+j],[[1],[1],[2],whatever])):
        #         normalsucc+=4
        #     elif (octojudger2(octo[color][i+j],[[0],[1],[2],whatever])):
        #         normalsucc+=3
        #     elif (octojudger2(octo[color][i+j],[[0],[0],[0],[1]])):
        #         normalsucc+=2
        #     elif (octojudger2(octo[color][i+j],[[0],[0],[2],[1]])):
        #         normalsucc+=1
        #     else:
        #         useless+=1 if octo[color][i+j]['neighbor']==1 else 0
    if numhuoer + nummiansan >= 1.9 and nummiansan >= 0.9:
        scoretable[x] += SCORE[SCORE_LEVEL - color - 2]
        chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 2 - color]

    elif numhuoer >= 1.9 and nummiansan == 0:
        scoretable[x] += SCORE[SCORE_LEVEL - color - 4]
        chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 4 - color]

    elif nummiansan == 0 or numhuoer == 0:
        scoretable[x] += (numhuoer + nummiansan) * SCORE[SCORE_LEVEL - color - 6]
        chessboardscore += (color * (-2) + 1) * SCORE[SCORE_LEVEL - 6 - color]

    scoretable[x] += ((numhuoyi + nummianer) * SCORE[SCORE_LEVEL - color - 8] + nummianyi * SCORE[SCORE_LEVEL - color - 10])
    chessboardscore += (color * (-2) + 1) * ((numhuoyi + nummianer) * SCORE[SCORE_LEVEL - 8 - color] + nummianyi * SCORE[SCORE_LEVEL - 10 - color])

    print("color",color)
    print("numhuoer",numhuoer)
    print("nummiansan",nummiansan)
    print("normalsucc",normalsucc)
    print("useless",useless)
    print("nummianer",nummianer)
    print("nummianyi",nummianyi)
    print("numhuoyi",numhuoyi)
    print()
