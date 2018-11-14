#! /usr/bin/python3
import sys
import copy

Cliques=[
#Left to Right
[0,1,2,3,4,5,6,7,8],\
[9,10,11,12,13,14,15,16,17],\
[18,19,20,21,22,23,24,25,26],\
[27,28,29,30,31,32,33,34,35],\
[36,37,38,39,40,41,42,43,44],\
[45,46,47,48,49,50,51,52,53],\
[54,55,56,57,58,59,60,61,62],\
[63,64,65,66,67,68,69,70,71],\
[72,73,74,75,76,77,78,79,80,],\
#Top to Bottom
[0,9,18,27,36,45,54,63,72],\
[1,10,19,28,37,46,55,64,73],\
[2,11,20,29,38,47,56,65,74],\
[3,12,21,30,39,48,57,66,75],\
[4,13,22,31,40,49,58,67,76],\
[5,14,23,32,41,50,59,68,77],\
[6,15,24,33,42,51,60,69,78],\
[7,16,25,34,43,52,61,70,79],\
[8,17,26,35,44,53,62,71,80],\
#Boxes in order
[0,1,2,9,10,11,18,19,20],\
[3,4,5,12,13,14,21,22,23],\
[6,7,8,15,16,17,24,25,26],\
[27,28,29,36,37,38,45,46,47],\
[30,31,32,39,40,41,48,49,50],\
[33,34,35,42,43,44,51,52,53],\
[54,55,56,63,64,65,72,73,74],\
[57,58,59,66,67,68,75,76,77],\
[60,61,62,69,70,71,78,79,80]\
]

positions = {}
#Returns the coordinates of left to right neighbors given a current num
def retlrneighbors(num):
    inorder = []
    for x in range(0,9):
        if (num in Cliques[x]):
            for val in Cliques[x]:
                if (val != num):
                    inorder.append([int(val/9),val%9])
    return inorder
#Returns the coordinates of top to bottom neighbors given a current num
def rettbneighbors(num):
    topbot = []
    for x in range(9,18):
        if (num in Cliques[x]):
            for val in Cliques[x]:
                if (val != num):
                    topbot.append([int(val/9),val%9])
    return topbot

def retboxnieghbors(num):
    box = []
    for i in range(18,27):
        if (num in Cliques[i]):
            for x in Cliques[i]:
                if (x != num):
                    box.append([int(x/9),x%9])
    return box


for i in range (0,81):
    positions[i] = [
    retlrneighbors(i),
    rettbneighbors(i),
    retboxnieghbors(i),
    ]
print(rettbneighbors(18))
#print (positions)
#print (rettbneighbors(0))
print(Cliques[9])
print(18 in Cliques[9])
#Now that I have all the positions, I want to convert each given sudoku board into a 2d array
input = open(sys.argv[1],'r').read().split("\n")
output = open(sys.argv[2],'w')
namepos = 0
while input[namepos] != sys.argv[3]:
    namepos += 1
start = namepos + 1
end = namepos + 9
finalNameArr = input[namepos].split(',')
finalName = finalNameArr[0] + ',' + finalNameArr[1] + ',solved\n'
board = []
for x in range(start,end + 1):
    boardIn = input[x].split(",")
    final = []
    for y in boardIn:
        if y != '_':
            final.append(int(y))
        else:
            final.append(0)
    board.append(final)
#print(finalName)
#print(board)

def safeRow(cell,num):
    if (board[int(cell/9)][cell%9] == num or board[int(cell/9)][cell%9] != 0):
        return False
    rows = positions[cell][0]
    #print(rows)
    #Check every other cell in my row
    for x in rows:
        if (board[x[0]][x[1]] == num):
            return False
    return True

def safeCol(cell,num):
    if (board[int(cell/9)][cell%9] == num or board[int(cell/9)][cell%9] != 0):
        return False
    col = positions[cell][1]
    for x in col:
        if (board[x[0]][x[1]] == num):
            return False
    return True

def safeBox(cell,num):
    if (board[int(cell/9)][cell%9] == num or board[int(cell/9)][cell%9] != 0):
        return False
    boxes = positions[cell][2]
    for x in boxes:
        if (board[x[0]][x[1]] == num):
            return False
    return True

def safe(cell,num):
    if safeRow(cell,num) and safeCol(cell,num) and safeBox(cell,num):
        return True
    return False
#print(safe(1,6))
#print(safeBox(1,9))
def isSolved():
    for row in range(0,9):
        for col in range(0,9):
            cellNum = row * 9 + col
            if(board[row][col] == 0):
                return False
    return True

def solve():
    #If my board has been cleared, return True
    if isSolved():
        return True
    numbers = [1,2,3,4,5,6,7,8,9]
    for row in range(0,9):
        for column in range(0,9):
            #For each index in 2D array, Test if each number works
            if board[row][column] == 0:
                cellNum = row * 9 + column
                for num in numbers:
                #   For my numbers, if it is safe to place, place it
                    if (safe(cellNum,num)):
                        board[row][column] = num
                        #If I solve the board, stop and return true
                        #print(board)
                        if solve():
                            return True
                        #otherwise, erase my change and test other values
                        board[row][column] = 0
                return False
#print(board)
solve()

output.write(finalName)
for r in range(0,9):
    for c in range(0,9):
        if c == 0 or c % 8 != 0:
            line = str(board[r][c]) + ","
        else:
            line = str(board[r][c]) + "\n"
        output.write(line)
#print(safe(9,2))
