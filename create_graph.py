import math
import random
import matplotlib.pyplot as plt

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


def scoring(solution):
    score = 0
    for q in range(LENGTH-1):
        for j in range(q+1, LENGTH):
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
    current_energy = scoring(current_sol)
    best_sol = current_sol
    best_energy = current_energy
    timer = 1
    while (temperature > final_temp) and (timer != max_step):
        for i in range(steps_per_change):
            try:
                step_sol = current_sol.copy()
                step_sol = my_shuffle(step_sol).copy()
                step_energy = scoring(step_sol)
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
    return timer, best_energy

T = 80
FINAL_TEMP = 0.1
STEPS_PER_CHANGE = 0
MAX_STEP = 10000
ALPHA = 0.99
LENGTH = 40
temperature_all = []
time = [0] * 5
energy = [0] * 5
bad_work = [0] * 5

for i in range(5):
    time_temp = 0
    energy_temp = 0
    temperature_all.append(100-i*2)
    for j in range(20):
        time_temp, energy_temp = annealing(100-i*2, FINAL_TEMP, STEPS_PER_CHANGE, MAX_STEP, ALPHA, LENGTH)
        if energy_temp != 0:
            bad_work[i] += 1
    time[i] = time_temp/20
    energy[i] = energy_temp/20

plt.title('')
plt.xlabel('temperature')
plt.ylabel('errors count')
plt.grid()
plt.plot(temperature_all, bad_work)
plt.show()

plt.title('')
plt.xlabel('temperature')
plt.ylabel('time')
plt.grid()
plt.plot(temperature_all, time)
plt.show()

plt.title('')
plt.xlabel('temperature')
plt.ylabel('means energy')
plt.grid()
plt.plot(temperature_all, energy)
plt.show()

steps_per_change_all = []
for i in range(5):
    steps_per_change_all.append(STEPS_PER_CHANGE)
    time_temp = 0
    energy_temp = 0
    for j in range(20):
        t, y = annealing(T, FINAL_TEMP, STEPS_PER_CHANGE, MAX_STEP, ALPHA, LENGTH)
        time_temp += t
        energy_temp += y
        if energy_temp != 0:
            bad_work[i] += 1
    time[i] = time_temp/20
    energy[i] = energy_temp/20
    STEPS_PER_CHANGE += 10


plt.title('')
plt.xlabel('steps per changed')
plt.ylabel('errors count')
plt.grid()
plt.plot(steps_per_change_all, bad_work)
plt.show()

plt.title('')
plt.xlabel('steps per changed')
plt.ylabel('time')
plt.grid()
plt.plot(steps_per_change_all, time)
plt.show()

plt.title('')
plt.xlabel('steps per changed')
plt.ylabel('means energy')
plt.grid()
plt.plot(steps_per_change_all, energy)
plt.show()