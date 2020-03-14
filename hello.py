import os
import sys
import subprocess as sp
import random
import datetime
from sqlite3 import *

conn = connect("2048.db")
curs = conn.cursor()
# creating the leaderboard table if it does not exist
sql_table = """
    CREATE TABLE LEADERBOARD (
        name text,
        created timestamp,
        score integer
    )
"""
try:
    curs.execute(sql_table)
except OperationalError:
    pass
except:
    print("Some unexpected error occured. Aborting!")
    sys.exit()

# Game class to initialize a new game
class Game:
    # __init__() initializes the create board for a game
    def __init__(self):
        # emptyPos contains all the empty positions in the board
        self.board = [[], [], [], []]
        for i in range(4):
            for j in range(4):
                self.board[i].append(" ")
        # in all the random choice functions, self.newElemList is used which contains 9 unit 2's and 1 4
        self.newElemList = []
        for i in range(9):
            self.newElemList.append(2)
        self.newElemList.append(4)
        self.score = 0

    def fillRandomBox(self):
        emptyPos = []
        for i in range(4):
            for j in range(4):
                if (self.board[i][j] == " "):
                    emptyPos.append(str(i)+str(j))
        pos = random.choice(range(len(emptyPos)))
        self.board[int(emptyPos[pos][0])][int(emptyPos[pos][1])] = random.choice(self.newElemList)

    # isFull return true if no empty blocks left
    def isFull(self):
        ans = 0
        for i in range(4):
            for j in range(4):
                if (self.board[i][j] == " "):
                    return False
        return True

    # validMoveLeft returns true if a valid move is left
    def validMoveLeft(self):
        for i in range(4):
            for j in range(4):
                if (self.board[i][j] == " "):
                    return True
        for i in range(4):
            for j in range(3):
                if (self.board[i][j] == self.board[i][j+1]):
                    return True
        for i in range(3):
            for j in range(4):
                if (self.board[i][j] == self.board[i+1][j]):
                    return True
        return False

    # newGame() clears the board for a new game
    def newGame(self):
        self.score = 0
        for i in range(4):
            for j in range(4):
                self.board[i][j] = " "
        # fill two random blocks in the board
        self.fillRandomBox()
        self.fillRandomBox()

        while((not self.isFull()) or (self.validMoveLeft())):
            sp.call("clear", shell=True)
            print("Controls: W, A, S, D")
            print("Q to quit the current game")
            self.printBoard()
            # ask for a move
            moved = False
            inp = input("Enter next move:")
            inp = inp.upper()
            if (inp == "W"):
                moved = self.moveUp()
            elif (inp == "S"):
                moved = self.moveDown()
            elif (inp == "A"):
                moved = self.moveLeft()
            elif (inp == "D"):
                moved = self.moveRight()
            elif (inp == "Q"):
                return
            else:
                print("Invalid Move!")
                os.system("pause")
                continue
            if (not moved):
                continue
            # a valid move was played
            if (not self.isFull()):
                self.fillRandomBox()

        sp.call("clear", shell=True)
        self.printBoard()
        print("Game Over!")
        print("Final Score: " + str(self.score))
        user = input("Enter your username to store the result, or press enter to skip.")
        if (user == ""):
            return
        # save the current user in the database with the highscore
        sql_table = """INSERT INTO 'LEADERBOARD'
                          ('name', 'created', 'score') 
                          VALUES (?, ?, ?);"""
        data_tuple = (user, datetime.datetime.now(), self.score)
        curs.execute(sql_table, data_tuple)
        conn.commit()

    # printBoard() prints the board to the console
    def printBoard(self):
        print("Current Score: " + str(self.score))
        for i in range(4):
            for j in range(4):
                print(str(self.board[i][j]) + " ", end="")
                if (j < 3):
                    print("| ", end="")
            print("\n", end="")
            if (i != 3):
                print("---------------")

    def moveUp(self):
        moved = False
        for j in range(4):
            # j denotes the column
            tempList = []
            for i in range(4):
                if (self.board[i][j] != " "):
                    tempList.append(self.board[i][j])
                    self.board[i][j] = " "
                    if (len(tempList)-1 < i):
                        moved = True
            for i in range(len(tempList) - 1):
                if (tempList[i] == tempList[i+1]):
                    tempList[i] *= 2
                    self.score += tempList[i]
                    tempList[i+1] = 0
                    moved = True
            ind = 0
            for i in range(len(tempList)):
                if (tempList[i] != 0):
                    self.board[ind][j] = tempList[i]
                    ind += 1
        return moved

    def moveDown(self):
        moved = False
        for j in range(4):
            # j denotes column
            tempList = []
            for i in range(3,-1,-1):
                if (self.board[i][j] != " "):
                    tempList.append(self.board[i][j])
                    self.board[i][j] = " "
                    if (len(tempList)-1 < 3-i):
                        moved = True
            for i in range(len(tempList) - 1):
                if (tempList[i] == tempList[i+1]):
                    tempList[i] *= 2
                    self.score += tempList[i]
                    tempList[i+1] = 0
                    moved = True
            ind = 3
            for i in range(len(tempList)):
                if (tempList[i] != 0):
                    self.board[ind][j] = tempList[i]
                    ind -= 1
        return moved

    def moveLeft(self):
        moved = False
        for i in range(4):
            # i denotes row
            tempList = []
            for j in range(4):
                if (self.board[i][j] != " "):
                    tempList.append(self.board[i][j])
                    self.board[i][j] = " "
                    if (len(tempList)-1 < j):
                        moved = True
            for j in range(len(tempList) - 1):
                if (tempList[j] == tempList[j+1]):
                    tempList[j] *= 2
                    self.score += tempList[j]
                    tempList[j+1] = 0
                    moved = True
            ind = 0
            for j in range(len(tempList)):
                if (tempList[j] != 0):
                    self.board[i][ind] = tempList[j]
                    ind += 1
        return moved

    def moveRight(self):
        moved = False
        for i in range(4):
            # i denotes row
            tempList = []
            for j in range(3,-1,-1):
                if (self.board[i][j] != " "):
                    tempList.append(self.board[i][j])
                    self.board[i][j] = " "
                    if (len(tempList)-1 < 3-j):
                        moved = True
            for j in range(len(tempList) - 1):
                if (tempList[j] == tempList[j+1]):
                    tempList[j] *= 2
                    self.score += tempList[j]
                    tempList[j+1] = 0
                    moved = True
            ind = 3
            for j in range(len(tempList)):
                if (tempList[j] != 0):
                    self.board[i][ind] = tempList[j]
                    ind -= 1
        return moved


def main():
    sp.call("clear", shell=True)
    game = Game()
    while(True):
        ans = input("Play? y/n (type lb for leaderboard)\n")
        if (ans.lower() == "lb"):
            sp.call("clear", shell=True)
            curs.execute("SELECT * from leaderboard ORDER BY score DESC, created ASC")
            ans = curs.fetchall()
            print("Current Leaderboard:\n")
            for i in ans:
                print(i)
            continue
        elif (ans.lower() == "n"):
            break
        elif (ans.lower() != "y"):
            sp.call("clear", shell=True)
            print("enter a valid option.")
            continue
        game.newGame()

main()
