import random
from typing import Callable, List

import tqdm
import numpy as np
import numba # Compiles python functions to C++: ~100X speedup

@numba.jit(nopython=True)
def chase_variance_strategy(score: int) -> int:
    """
    Idea behind solution.
    Both 1 point, and 2 point flips have EV: 0
    BUT, 1 point has stdev of 1 and 2 points has stdev of 2
    If you are already winning you should try and minimize stdev so that you are
    less likely to go into the negative (thus choose 1 point)
    If you are losing you should try and maximize stdev so that you are more
    likely to go into the positive (thus choose 2 points)
    """
    if score > 0:
        return 1
    return 2

@numba.jit(nopython=True)
def always_1_strategy(_: int) -> int:
    return 1

@numba.jit(nopython=True)
def always_2_strategy(_:int) -> int:
    return 2

@numba.jit(nopython=True)
def choose_randomly_strategy(_:int) -> int:
    return random.randint(1,2)

@numba.jit(nopython=True)
def simulate(strategy: Callable[[int], int]) -> int:
    points = 0
    for _ in range(101):
        point_delta = strategy(points)

        if random.randint(0,1):
            points += point_delta
        else:
            points -= point_delta

    return points

def summarize_outcomes(outcomes: List[int]):
    expected_point_value = np.mean(outcomes)
    win_loss = sum([1 if x > 0 else 0 for x in outcomes])

    print(f'EV: {expected_point_value}\n'
          f'WinRate: {win_loss / len(outcomes)}\n'
          f'StdDev: {np.std(outcomes)}')


SIMULATIONS = 1_000_000

variance_outcomes = []
for _ in tqdm.tqdm(range(SIMULATIONS), desc='Variance'):
    variance_outcomes.append(simulate(chase_variance_strategy))

always_1_outcomes = []
for _ in tqdm.tqdm(range(SIMULATIONS), desc='Always 1'):
    always_1_outcomes.append(simulate(always_1_strategy))


always_2_outcomes = []
for _ in tqdm.tqdm(range(SIMULATIONS), desc='Always 2'):
    always_2_outcomes.append(simulate(always_2_strategy))

choose_randomly_outcomes = []
for _ in tqdm.tqdm(range(SIMULATIONS), desc= 'Random'):
    choose_randomly_outcomes.append(simulate(choose_randomly_strategy))

print('\nVariance Strategy Summary:')
summarize_outcomes(variance_outcomes)

print('\nAlways 1 Strategy Summary:')
summarize_outcomes(always_1_outcomes)

print('\nAlways 2 Strategy Summary:')
summarize_outcomes(always_2_outcomes)

print('\nRandom Strategy Summary:')
summarize_outcomes(choose_randomly_outcomes)

## OUTPUT ##
# Variance Strategy Summary:
# EV: -0.002921
# WinRate: 0.640157
# StdDev: 14.776872012295396
# 
# Always 1 Strategy Summary:
# EV: -0.005034
# WinRate: 0.499948
# StdDev: 10.058231189371421
# 
# Always 2 Strategy Summary:
# EV: -0.044724
# WinRate: 0.498846
# StdDev: 20.088952181829296
# 
# Random Strategy Summary:
# EV: -0.048723
# WinRate: 0.486215
# StdDev: 15.880893585351892
