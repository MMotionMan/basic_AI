import math
import random
from datetime import datetime

random.seed(42)
time = datetime.now()



def my_shuffle(solution):
    first = random.randint(0, len(solution)-1)
    second = random.randint(0, len(solution)-1)
    solution[first], solution[second] = solution[second], solution[first]
    return solution


def output_board(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            print(board[i][j], end=' ')
        print(end='\n')


def scoring(solution, length):
    score = 0
    for q in range(length-1):
        for j in range(q+1, length):
            # print(abs(solution[q] - solution[j]), '|', abs(q-j), '|', q, '|', j)
            if abs(solution[q] - solution[j]) == abs(q-j):
                score += 1
    return score


def make_board(solution):
    t = [[0 for q in range(len(solution))] for j in range(len(solution))]
    for q in range(len(solution)):
        t[solution[q]][q] = 1
    return t


def decrease_temperature(temperature, k):
    return temperature * k


def annealing(temperature, final_temp, steps_per_change, max_step, alpha, length):
    current_sol = [i for i in range(length)]
    random.shuffle(current_sol)
    current_energy = scoring(current_sol, length)
    best_sol = current_sol
    best_energy = current_energy
    timer = 1
    while (temperature > final_temp) and (timer != max_step):
        for i in range(steps_per_change):
            try:
                step_sol = current_sol.copy()
                step_sol = my_shuffle(step_sol).copy()
                step_energy = scoring(step_sol, length)
                p = math.exp(-(current_energy - step_energy) / temperature)
                if step_energy < current_energy:
                    current_sol = step_sol.copy()
                    current_energy = step_energy
                    if step_energy < best_energy:
                        best_sol = step_sol.copy()
                        best_energy = step_energy
                elif p > random.random():
                    current_sol = step_sol.copy()
            except OverflowError:
                print('OverflowError')
        current_sol = best_sol.copy()
        temperature = decrease_temperature(temperature, alpha)
        timer += 1
    return make_board(best_sol), best_energy




T = 120
FINAL_TEMP = 0.1
STEPS_PER_CHANGE = 1000
MAX_STEP = 10000
ALPHA = 0.99
LENGTH = 40
print(annealing(T, FINAL_TEMP, STEPS_PER_CHANGE, MAX_STEP, ALPHA, LENGTH))
print(f'{datetime.now() - time} сек')