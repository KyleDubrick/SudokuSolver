import random
import copy
import math
import time

counter = 0
time_to_complete = 0

#Test cases
easy = [[0 for x in range(9)] for y in range(9)]
medium = [[0 for x in range(9)] for y in range(9)]
hard = [[0 for x in range(9)] for y in range(9)]
evil = [[0 for x in range(9)] for y in range(9)]

easy[0][2] = easy[1][8] = easy[4][5] = easy[7][0] = medium[0][4] = medium[2][0] = medium[3][5] = hard[2][8] = hard[3][1] = evil[1][8] = evil[5][5] = 1
easy[0][8] = easy[3][5] = easy[5][6] = easy[8][1] = medium[1][1] = medium[3][4] = medium[6][8] = hard[0][4] = hard[6][1] = evil[0][4] = evil[1][2] = evil[5][0] = evil[6][1] = evil[8][7] = 2
easy[3][2] = easy[5][5] = easy[8][7] = medium[2][8] = medium[5][3] = medium[6][2] = medium[7][4] = hard[1][4] = hard[5][7] = evil[4][7] = 3
easy[2][6] = easy[3][7] = easy[6][2] = medium[1][3] = medium[4][0] = hard[0][1] = hard[1][7] = hard[4][5] = hard[6][0] = hard[7][4] = evil[3][0] = evil[7][2] = evil[8][4] = 4
easy[0][7] = easy[2][3] = easy[4][6] = easy[5][0] = easy[6][8] = medium[0][0] = medium[1][4] = medium[2][6] = medium[8][8] = hard[0][5] = hard[4][4] = hard[7][3] = hard[8][7] = evil[2][7] = evil[3][3] = 5
easy[0][1] = easy[3][3] = easy[4][2] = easy[5][8] = easy[8][0] = medium[0][3] = medium[4][8] = medium[5][4] = medium[7][2] = medium[8][5] = hard[2][7] = hard[4][0] = hard[8][4] = evil[0][1] = evil[3][8] = evil[4][3] = 6
easy[2][0] = easy[3][8] = easy[4][3] = easy[5][1] = medium[1][5] = medium[7][3] = hard[3][2] = hard[4][3] = hard[5][6] = evil[2][3] = evil[4][5] = evil[5][8] = evil[7][6] = 7
easy[1][0] = easy[7][8] = medium[1][6] = medium[7][7] = medium[8][4] = hard[8][2] = evil[0][3] = evil[1][6] = evil[7][0] = evil[8][5] = 8
easy[3][0] = easy[5][3] = easy[6][5] = easy[8][6] = medium[6][0] = medium[7][5] = hard[0][6] = hard[1][5] = hard[4][8] = hard[7][1] = hard[8][3] = evil[4][1] = evil[6][5] = 9

def csp_checker(x, y, state, value):
    for i in range(9):
        if state[i][y] == value:
            return 0
    for j in range(9):
        if state[x][j] == value:
            return 0
    for k in range(math.ceil((x + 1) / 3) * 3 - 3, math.ceil((x + 1) / 3) * 3):
        for l in range(math.ceil((y + 1) / 3) * 3 - 3, math.ceil((y + 1) / 3) * 3):
            if state[k][l] == value:
                return 0
    return 1


def backtrack_search(state):
    start_time = time.time()
    variables = []
    global time_to_complete
    for i in range(9):
        for j in range(9):
            if state[i][j] == 0:
                variables.append([i, j])
    random.shuffle(variables, random.random)
    answer = backtrack(state, variables)
    time_to_complete = (time.time() - start_time)
    # print("{0} Seconds" .format(time_to_complete))
    # print(counter)
    return answer


def backtrack(stateRef, variablesRef):
    state = [row[:] for row in stateRef]
    variables = [row[:] for row in variablesRef]
    global counter
    counter = counter + 1
    if (counter % 1000000) == 0:
        print(counter)
    if not variables:
        return state
    values = list(range(1, 10))
    random.shuffle(values, random.random)
    variable = variables.pop()
    success = 0
    for i in range(9):
        value = values.pop()
        if csp_checker(variable[0], variable[1], state, value) == 1:
            state[variable[0]][variable[1]] = value
            success = backtrack(state, variables)
        if success != 0:
            return success
    return success


def evaluation_loop(state, amount):
    time_total = 0
    counter_total = 0
    times = []
    counters = []
    global counter
    global time_to_complete
    for x in range(amount):
        if backtrack_search(state) == 0:
            return 0
        time_total = time_total + time_to_complete
        counter_total = counter_total + counter
        times.append(time_to_complete)
        counters.append(counter)
        counter = 0
        time_to_complete = 0
        # percent = ((100 / amount) * (x + 1))
        # print('{0} percent done' .format(percent))
    average_nodes = counter_total / amount
    average_time = time_total / amount
    cstd = 0
    tstd = 0
    for x in counters:
        cstd = cstd + (average_nodes - x) * (average_nodes - x)
    cstd = cstd / amount
    cstd = math.sqrt(cstd)
    for x in times:
        tstd = tstd + (average_time - x) * (average_time - x)
    tstd = tstd / amount
    tstd = math.sqrt(tstd)
    print("Average nodes visited: {0}".format(average_nodes))
    print("Average time taken: {0}".format(average_time))
    print("Node std: {0}".format(cstd))
    print("time std: {0}".format(tstd))
    return 1