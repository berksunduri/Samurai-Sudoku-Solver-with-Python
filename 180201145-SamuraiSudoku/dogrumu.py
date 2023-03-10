
digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits


def dogrumu(values, sqrs):

    samurai = []
    for sqr in sqrs:
        samurai.append(generateSudo(values, sqr))

    for sudoku in samurai:
        if not checkSudo(sudoku):
            print("Sudoku yanlis.")
            return False

    corners_coordinate = [
        [[samurai[0], [6, 6]], [samurai[4], [0, 0]]],
        [[samurai[1], [6, 0]], [samurai[4], [0, 6]]],
        [[samurai[2], [0, 6]], [samurai[4], [6, 0]]],
        [[samurai[3], [0, 0]], [samurai[4], [6, 6]]]
    ]

    for corner in corners_coordinate:
        if not checkCor(corner[0], corner[1]):
            print("Sudoku Yanlis")
            return False

    print("Cozum Dogru")
    return True

def checkSudo(sudoku):


    box_coordinate = [
        [[0, 0], [0, 3], [0, 6]],
        [[3, 0], [3, 3], [3, 6]],
        [[6, 0], [6, 3], [6, 6]]
    ]

    for row in box_coordinate:
        for col in row:
            box = getBox(sudoku, col[0], col[1])
            if not checkUniqueList(matrixTolist(box)):
                return False


    for row in sudoku:
        if not checkUniqueList(row):
            return False


    for col in range(9):
        col_list = []
        for row in range(9):
            col_list.append(sudoku[row][col])
        if not checkUniqueList(col_list):
            return False

    return True


def checkCor(box1, box2):

    box1_list = getBox(box1[0], box1[1][0], box1[1][1])
    box2_list = getBox(box2[0], box2[1][0], box2[1][1])
    return box1_list == box2_list


def checkUniqueList(input):
    int_list = list(map(int, input))
    int_list.sort()
    return int_list == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def generateSudo(values, sqr):

    sudoku = [[None]*9]*9
    i = 0
    for r in rows:
        sudoku[i] = [values[sqr[(ord(r) - 65) * 9 + int(c) - 1]] for c in cols]
        i += 1
        if i == 9:
            i = 0
    return sudoku


def getBox(sudoku, row, col):

    box = [[]*3]*3
    count = 3
    for i in range(len(box)):
        box[i] = sudoku[row][col:col+3]
        row += 1
    return box
def matrixTolist(matrix):

    return [val for sublist in matrix for val in sublist]
