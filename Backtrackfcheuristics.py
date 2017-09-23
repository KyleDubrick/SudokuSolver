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
    for k in range(math.ceil((x + 1)/3) * 3 - 3, math.ceil((x + 1)/3) * 3):
        for l in range(math.ceil((y + 1)/3) * 3 - 3, math.ceil((y + 1)/3) * 3):
            if state[k][l] == value:
                return 0
    return 1


def backtrack_search(state):
    start_time = time.time()
    variables = []
    global time_to_complete
    fc = [[[1 for x in range(9)] for y in range(9)] for z in range(9)]
    fcsum = [[9 for x in range(9)] for y in range(9)]
    values = [[x + 1, 0] for x in range(9)]
    for i in range (9):
        for j in range (9):
            if state[i][j] == 0:
                variables.append([i, j, 0, 20])
    for i in range (9):
        for j in range (9):            
            if state[i][j] != 0:
                fcar = forwardcheck(fc, state, i, j, state[i][j], fcsum, variables)
                fc = fcar[0]
                fcsum = fcar[1]
    #print(fcsum)
    #print(fc)
    answer = backtrack(state, variables, fc, fcsum, values)
    time_to_complete = (time.time() - start_time)
    #print("{0} Seconds" .format(time_to_complete))
    #print(counter)
    return answer


def backtrack(stateRef, variablesRef, fcRef, fcsumRef, valuesRef):
    state = [row[:] for row in stateRef]
    variables = [row[:] for row in variablesRef]
    fc = [[x[:] for x in y] for y in fcRef]
    fcsum = [x[:] for x in fcsumRef]
    global counter
    #if (counter % 1000000) == 0:
    counter = counter + 1
    if not variables:
        return state
    values = [x[:] for x in valuesRef]
    useablevalues = [x[:] for x in valuesRef]
    variable = variables.pop(variable_chooser(variables))
    unchangedvariables = [x[:] for x in variables]
    success = 0
    for i in range(9):
        value = useablevalues.pop(value_chooser(useablevalues))
        if csp_checker(variable[0], variable[1], state, value[0]) == 1:
            checker = forwardcheck(fc, state, variable[0], variable[1], value[0], fcsum, variables)
            if checker:
                fc = checker[0]
                fcsum = checker[1]
                variables = checker[2]
                state[variable[0]][variable[1]] = value[0]
                values[value[0] - 1][1] = values[value[0] - 1][1] + 1
                success = backtrack(state, variables, fc, fcsum, values)
        if success != 0:
            return success
        else:
            state[variable[0]][variable[1]] = 0
            fc = [[x[:] for x in y] for y in fcRef]
            fcsum = [x[:] for x in fcsumRef]
            variables = [row[:] for row in unchangedvariables]
            values = [x[:] for x in valuesRef]
    return success

def forwardcheck(oldfc, state, i, j, value, oldfcsum, oldvariables):
    fc = [[x[:] for x in y] for y in oldfc]
    fcsum = [x[:] for x in oldfcsum]
    variables = [x[:] for x in oldvariables]
    sum = 0
    for x in range (9):
        if fc[x][j][value - 1] == 1:
            fcsum[x][j] = oldfcsum[x][j] - 1
            fc[x][j][value - 1] = 0
            if (state[x][j] == 0) and (fcsum[x][j] == 0) and (x != i):
                return 0
    for y in range(9):
        if fc[i][y][value - 1] == 1:
            fcsum[i][y] = oldfcsum[i][y] - 1
            fc[i][y][value - 1] = 0
            if (state[i][y] == 0) and (fcsum[i][y] == 0) and (y != j):
                return 0            
    for k in range(math.ceil((i + 1)/3) * 3 - 3, math.ceil((i + 1)/3)*3):
        for l in range(math.ceil((j + 1)/3) * 3 - 3, math.ceil((j + 1)/3) * 3):
            if fc[k][l][value - 1] == 1:
                fcsum[k][l] = oldfcsum[k][l] - 1
                fc[k][l][value - 1] = 0
                if (state[k][l] == 0) and (fcsum[k][l] == 0) and (k != i) and (l != j):
                    return 0
    for x in variables:
        if x[0] == i or x[1] == j or (math.ceil(x[0] + 1) == math.ceil(i + 1) and math.ceil(x[1] + 1) == math.ceil(j + 1)):
            x[2] = 9 - fcsum[x[0]][x[1]]
            x[3] = x[3] - 1
    return [fc, fcsum, variables]

def variable_chooser(variables):
    choice = 0
    index = 0
    for x in variables:
        if variables[choice][2] < x[2]:
            choice = index
        if variables[choice][2] == x[2]:
            if variables[choice][3] < x[3]:
                choice = index
            if variables[choice][3] == x[3]:
                r = random.randint(0, 1)
                if r == 0:
                    choice = index
        index = index + 1
    return choice

def value_chooser(values):
    choice = 0
    index = 0
    for x in values:
        if values[choice][1] < x[1]:
            choice = index
        if values[choice][1] == x[1]:
            r = random.randint(0, 1)
            if r == 0:
                choice = index
        index = index + 1
    return choice

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
        #percent = ((100 / amount) * (x + 1))
        #print('{0} percent done' .format(percent))
    average_nodes = counter_total / amount
    average_time = time_total / amount
    cstd = 0
    tstd = 0
    for x in counters:
        cstd = cstd + (average_nodes - x) * (average_nodes - x)
    cstd = cstd/amount
    cstd = math.sqrt(cstd)
    for x in times:
        tstd = tstd + (average_time - x) * (average_time - x)
    tstd = tstd/amount
    tstd = math.sqrt(tstd)    
    print("Average nodes visited: {0}" .format(average_nodes))
    print("Average time taken: {0}" .format(average_time))
    print("Node std: {0}" .format(cstd))
    print("time std: {0}" .format(tstd))    
    return 1


def longtest():
    evaluation_loop(easy, 50)
    evaluation_loop(medium, 50)
    evaluation_loop(hard, 50)
    evaluation_loop(evil, 50)
    return 1

longtest()