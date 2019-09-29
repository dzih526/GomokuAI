#!/usr/bin/env python3
"""
check the security and functionability of uploaded code
- forbid from importing os
- random chessboard check
- some special case check
"""
import imp
import traceback
import sys
import os
import numpy as np
from timeout_decorator import timeout

FORBIDDEN_LIST = ['import os', 'exec']

class CodeCheck():
    def __init__(self, script_file_path, chessboard_size):
        self.time_out = 1000000
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None
        self.errormsg = 'Error'
        self.errorcase = 0
        # sys.stdout = open(os.devnull, 'w')
        # sys.stderr = open(os.devnull, 'w')
        # print(self.chessboard)

    # Call this function and get True or False, self.errormsg has the massage
    def check_code(self):
        # check if contains forbidden library
        if self.__check_forbidden_import() == False:
            return False

        # check initialization
        try:
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        except Exception:
            self.errormsg = "Fail to init"
            return False

        # check simple condition
        if not self.__check_simple_chessboard():
            self.errormsg = "Can not pass usability test."
            return False

        # check advance condition, online test contain more test case than this demo
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass base test."
            return False

        return True

    def __check_forbidden_import(self):
        with open(self.script_file_path, 'r', encoding='UTF-8') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True

    def __check_go(self, chessboard,color=-1):
        self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, color, self.time_out)
        try:
            timeout(self.time_out)(self.agent.go)(np.copy(chessboard))
        except Exception:
            self.errormsg = "Error:" + traceback.format_exc()
            return False
        return True

    def __check_result(self, chessboard, result,color=-1):
        if not self.__check_go(chessboard,color):
            return False
        if not self.agent.candidate_list or \
            list(self.agent.candidate_list[-1]) not in result:
            print("your result",self.agent.candidate_list[-1])
            print("the answer",result)
            return False
        print("your result",self.agent.candidate_list[-1])
        print("the answer",result)
        return True

    def __check_simple_chessboard(self):
        # empty chessboard
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            return False

        # only one empty position remain
        chessboard = np.ones((self.chessboard_size, self.chessboard_size))
        chessboard[:, ::2] = -1
        for i in range(0, self.chessboard_size, 4):
            chessboard[i] = -chessboard[i]
        x, y = np.random.choice(self.chessboard_size, 2)
        chessboard[x, y] = 0

        if not self.__check_result(chessboard, [[x, y]]):
            return False

        return True
    def readchessboard(self,filename,backstep=0):
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

    def __check_advance_chessboard(self):
        #
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[2, 2] = 1
        chessboard[3, 3] = 1
        chessboard[4, 4] = 1
        chessboard[5, 6] = 1
        chessboard[5, 8] = 1
        chessboard[1:3, 11] = -1
        chessboard[3, 9:11] = -1
        chessboard[6, 13] = -1
        if not self.__check_result(chessboard, [[5, 5]]):
            self.errorcase = 1
            return False

        #
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[2, 2:4] = 1
        chessboard[4, 1:3] = 1
        chessboard[1, 10:12] = -1
        chessboard[2, 10] = -1
        chessboard[4, 12] = -1
        if not self.__check_result(chessboard, [[1, 9]]):
            self.errorcase = 2
            return False

        #
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[2, 2] = 1
        chessboard[2, 4] = 1
        chessboard[3, 2:4] = 1
        chessboard[5, 2] = 1
        chessboard[1, 10:12] = -1
        chessboard[2, 10] = -1
        chessboard[4, 12:14] = -1
        if not self.__check_result(chessboard, [[4, 2]]):
            self.errorcase = 3
            return False

        #
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[2:5, 2] = 1
        chessboard[6, 3:5] = 1
        chessboard[1, 10:12] = -1
        chessboard[2, 10] = -1
        chessboard[4, 12:14] = -1
        if not self.__check_result(chessboard, [[5, 2]]):
            self.errorcase = 4
            return False

        #
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[1, 3] = 1
        chessboard[2, 2] = 1
        chessboard[2, 5] = 1
        chessboard[3:5, 3] = 1
        chessboard[1, 11:13] = -1
        chessboard[2, 11:13] = -1
        chessboard[5, 13] = -1
        if not self.__check_result(chessboard, [[2, 3]]):
            self.errorcase = 5
            return False

        chessboard = self.readchessboard("testcase/chess_log10_1_6-8_6.txt",6)
        if not self.__check_result(chessboard, [[8, 6],[12,5]],1):
            self.errorcase = 6
            return False

        chessboard = self.readchessboard("testcase/chess_log_secure.txt",2)
        if not self.__check_result(chessboard, [[4,9]],-1):
            self.errorcase = 6
            return False


        chessboard = self.readchessboard("testcase/chess_log_1_6_13_8.txt",6)
        if not self.__check_result(chessboard, [[13, 8],[10,11]],1):
            self.errorcase = 6
            return False

        chessboard = self.readchessboard("testcase/chess_log12_-1_6-7_12,11_8.txt",6)
        if not self.__check_result(chessboard, [[7, 12],[11,8],[4,10]],-1):
            self.errorcase = 6
            return

        chessboard = self.readchessboard("testcase/chess_log15_1_6-8_4.txt",6)
        if not self.__check_result(chessboard, [[8, 4]],-1):
            self.errorcase = 6
            return False

        chessboard = self.readchessboard("testcase/chess_log17_-1_6-5_4.txt",6)
        if not self.__check_result(chessboard, [[5, 4],[6,5]],-1):
            self.errorcase = 6
            return False

        chessboard = self.readchessboard("testcase/chess_log_secure.txt",2)
        if not self.__check_result(chessboard, [[4, 9]],-1):
            self.errorcase = 6
            return False

        return True
